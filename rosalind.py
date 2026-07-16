#!/usr/bin/env python

from argparse import ArgumentParser
from enum import StrEnum
from pathlib import Path
from shutil import copy
from subprocess import run


class RosalindError(Exception): ...


class Command(StrEnum):
    RUN = "run"
    CREATE = "create"


class Language(StrEnum):
    GO = "go"


class Input(StrEnum):
    SAMPLE = "sample"
    DATASET = "dataset"


RUN_COMMANDS: dict[Language, list[str]] = {
    Language.GO: ["go", "run"],
}

INPUT_FILES: dict[Input, str] = {
    Input.SAMPLE: "SAMPLE.txt",
    Input.DATASET: "DATASET.txt",
}

DEFAULT_LANGUAGE = Language.GO
DEFAULT_INPUT = Input.SAMPLE

ROOT_DIR = Path(__file__).resolve().parent
PROBLEMS_DIR = ROOT_DIR / "problems"
TEMPLATES_DIR = ROOT_DIR / "templates"


def problem_path(problem: str) -> Path:
    if not problem or not problem.isalpha():
        raise RosalindError(f"invalid problem id: {problem}")
    return PROBLEMS_DIR / problem


def template_path(language: Language) -> Path:
    return TEMPLATES_DIR / f"solution.{language}"


def solution_path(problem: str, language: Language) -> Path:
    return problem_path(problem) / f"solution.{language}"


def input_path(problem: str, input: Input) -> Path:
    return problem_path(problem) / INPUT_FILES[input]


def require_existing_file(path: Path) -> Path:
    if not path.is_file():
        raise RosalindError(f"file not found: {path}")
    return path


def require_missing_file(path: Path) -> Path:
    if path.is_file():
        raise RosalindError(f"file already exists: {path}")
    return path


def run_solution(problem: str, language: Language, input: Input) -> int:
    run_command = RUN_COMMANDS[language]

    solution_file = require_existing_file(solution_path(problem, language))
    input_file = require_existing_file(input_path(problem, input))

    with input_file.open() as stdin:
        try:
            process = run([*run_command, str(solution_file)], stdin=stdin)
        except FileNotFoundError:
            raise RosalindError(f"command not found: {run_command[0]}")

    return process.returncode


def create_solution(problem: str, language: Language) -> None:
    solution_file = require_missing_file(solution_path(problem, language))
    template_file = require_existing_file(template_path(language))

    problem_dir = problem_path(problem)
    problem_dir.mkdir(parents=True, exist_ok=True)

    for filename in INPUT_FILES.values():
        (problem_dir / filename).touch()

    copy(template_file, solution_file)


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Run and scaffold Rosalind problem solutions"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_problem_argument(subparser: ArgumentParser) -> None:
        subparser.add_argument("problem", help="problem id")

    def add_language_option(subparser: ArgumentParser) -> None:
        subparser.add_argument(
            "-l",
            "--language",
            type=Language,
            choices=Language,
            default=DEFAULT_LANGUAGE,
            help="solution language (default: %(default)s)",
        )

    def add_input_option(subparser: ArgumentParser) -> None:
        subparser.add_argument(
            "-i",
            "--input",
            type=Input,
            choices=Input,
            default=DEFAULT_INPUT,
            help="input source (default: %(default)s)",
        )

    run_parser = subparsers.add_parser(
        Command.RUN, help="run a problem solution"
    )
    add_problem_argument(run_parser)
    add_language_option(run_parser)
    add_input_option(run_parser)

    create_parser = subparsers.add_parser(
        Command.CREATE, help="scaffold a new problem solution"
    )
    add_problem_argument(create_parser)
    add_language_option(create_parser)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        match args.command:
            case Command.RUN:
                return run_solution(args.problem, args.language, args.input)
            case Command.CREATE:
                create_solution(args.problem, args.language)
                return 0
    except RosalindError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
