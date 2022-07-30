#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from .. enum.translation import Translation
from .. enum.card import Card
from .. base_generator import BaseGenerator


class SpanishGenerator(BaseGenerator):

    def get_formatted_words(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        raise NotImplementedError

    def generate_card(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:
        raise NotImplementedError
