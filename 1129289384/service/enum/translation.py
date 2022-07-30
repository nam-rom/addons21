#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List


class Translation:

    def __init__(self, source, target):

        self.source: str = source
        self.target: str = target

    def equals(self, translation) -> bool:
        if isinstance(translation, Translation):
            return self.target == translation.target and self.source == translation.source
        else:
            return False


def contains(translationList: List[Translation], translation: Translation) -> bool:
    for elem in translationList:
        if elem.equals(translation):
            return True

    return False
