#!/usr/bin/env python

from argparse import ArgumentParser
from enum import StrEnum
from pathlib import Path
from subprocess import run
from sys import exit
from textwrap import dedent
from typing import NamedTuple


class Command(StrEnum):
    RUN = "run"
    CREATE = "create"


class Language(StrEnum):
    GO = "go"


class Input(StrEnum):
    SAMPLE = "sample"
    DATASET = "dataset"


class LanguageConfig(NamedTuple):
    command: list[str]
    template: str


RUN_COMMANDS: dict[Language, list[str]] = {
    Language.GO: ["go", "run"],
}

DEFAULT_LANGUAGE = Language.GO
DEFAULT_INPUT = Input.SAMPLE

INPUT_FILES: dict[Input, str] = {
    Input.SAMPLE: "SAMPLE.txt",
    Input.DATASET: "DATASET.txt",
}

LANGUAGES: dict[Language, LanguageConfig] = {
    Language.GO: LanguageConfig(
        command=["go", "run"],
        template=dedent("""\
            package main

            import (
                "bufio"
                "fmt"
                "os"
            )

            func solve(s string) string {
                return s
            }

            func main() {
                s := bufio.NewScanner(os.Stdin)
                if !s.Scan() {
                    fmt.Fprintln(os.Stderr, "Error reading input:", s.Err())
                    os.Exit(1)
                }
                fmt.Println(solve(s.Text()))
            }
        """),
    )
}

ROOT_DIR = Path(__file__).resolve().parent
PROBLEMS_DIR = ROOT_DIR / "problems"
TEMPLATES_DIR = ROOT_DIR / "templates"


def solution_path(problem: str, language: Language) -> Path:
    return PROBLEMS_DIR / problem / f"solution.{language}"


def run_solution(problem: str, language: Language, input: Input) -> int:
    config = LANGUAGES[language]

    solution_file = solution_path(problem, language)
    if not solution_file.is_file():
        exit(f"missing {solution_file}")

    input_file = PROBLEMS_DIR / problem / INPUT_FILES[input]
    if not input_file.is_file():
        exit(f"missing {input_file}")

    with input_file.open() as stdin:
        try:
            process = run([*config.command, str(solution_file)], stdin=stdin)
        except FileNotFoundError:
            command = config.command[0]
            exit(f"{command} command not found")

    return process.returncode


def create_solution(problem: str, language: Language) -> None:
    config = LANGUAGES[language]

    solution_file = solution_path(problem, language)
    if solution_file.exists():
        exit(f"{solution_file} already exists")

    solution_file.parent.mkdir(parents=True, exist_ok=True)
    for filename in INPUT_FILES.values():
        (solution_file.parent / filename).touch()

    solution_file.write_text(config.template)
    print(f"{solution_file} created")


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


def main() -> None:
    args = build_parser().parse_args()

    match args.command:
        case Command.RUN:
            exit(run_solution(args.problem, args.language, args.input))
        case Command.CREATE:
            create_solution(args.problem, args.language)


if __name__ == "__main__":
    main()
