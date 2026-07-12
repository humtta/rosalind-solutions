#!/usr/bin/env python

from enum import StrEnum
from pathlib import Path
from textwrap import dedent
from typing import NamedTuple


class Language(StrEnum):
    GO = "go"


class Input(StrEnum):
    SAMPLE = "sample"
    DATASET = "dataset"


class LanguageConfig(NamedTuple):
    command: list[str]
    template: str


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

PROBLEMS_DIR = Path(__file__).resolve().parent / "problems"
