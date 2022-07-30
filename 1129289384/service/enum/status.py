#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Status:

    SUCCESS: str = "SUCCESS"

    CONNECTION_FAILED: str = "CONNECTION_FAILED"

    WORD_NOT_FOUND: str = "WORD_NOT_FOUND"

    NOT_SUPPORTED_TRANSLATION: str = "NOT_SUPPORTED_TRANSLATION"
