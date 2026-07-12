#!/usr/bin/env python

from enum import StrEnum


class Language(StrEnum):
    GO = "go"


class Input(StrEnum):
    SAMPLE = "sample"
    DATASET = "dataset"
