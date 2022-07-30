#!/usr/bin/python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from .. enum.translation import Translation


@dataclass
class Card:

    def __init__(self, word=None, wordId=None, oriWord=None, translation=None):

        self.word: str = word
        self.wordId: str = wordId
        self.oriWord: str = oriWord

        self.wordType: str = ""
        self.phonetic: str = ""
        self.example: str = ""

        self.image: str = ""
        self.sounds: str = ""
        self.status: str = ""

        self.meaning: str = ""
        self.copyright: str = ""
        self.comment: str = ""
        self.tag: str = ""

        self.translation: Translation = translation
