#!/usr/bin/env python

from enum import StrEnum
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
