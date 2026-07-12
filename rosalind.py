#!/usr/bin/env python

from enum import StrEnum


class Language(StrEnum):
    GO = "Go"


class Input(StrEnum):
    SAMPLE = "sample"
    DATASET = "dataset"
