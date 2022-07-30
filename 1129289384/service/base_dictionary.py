#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup
from . enum.translation import Translation


class BaseDictionary(ABC):

    def __init__(self):

        self.delimiter: str = "==="
        self.doc: BeautifulSoup = None

        self.word: str = ""
        self.wordId: str = ""
        self.oriWord: str = ""

        self.ankiDir: str = ""
        self.image: str = ""
        self.sounds: str = ""

        self.wordType: str = ""
        self.phonetic: str = ""

    @abstractmethod
    def search(self, formattedWord, translation: Translation) -> bool:
        """Find input word from dictionary data. Return True if Not Found"""
        raise NotImplementedError

    @abstractmethod
    def is_invalid_word(self) -> bool:
        """Check if the input word exists in dictionary?"""
        raise NotImplementedError

    @abstractmethod
    def get_word_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_example(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_phonetic(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_image(self, ankiDir: str, isOnline: bool) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_sounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_meaning(self) -> str:
        raise NotImplementedError

    def get_tag(self) -> str:
        return self.word[0]

    @abstractmethod
    def get_dictionary_name(self) -> str:
        raise NotImplementedError
