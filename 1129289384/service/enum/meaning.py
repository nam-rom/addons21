#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List


@dataclass
class Meaning:

    def __init__(self, meaning=None, examples=None):

        self.wordType: str = ""

        self.meaning: str = meaning

        self.subMeaning: str = ""

        self.examples: List[str] = examples
