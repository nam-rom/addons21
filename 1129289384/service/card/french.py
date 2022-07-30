#!/usr/bin/python
# -*- coding: utf-8 -*-


from typing import List

from .. enum.translation import Translation
from .. enum.card import Card
from .. enum.status import Status
from .. constant import Constant
from .. base_generator import BaseGenerator

from .. dictionary.collins import CollinsDictionary
from .. dictionary.lacviet import LacVietDictionary


class FrenchGenerator(BaseGenerator):

    def get_formatted_words(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        word = word.lower().strip()
        foundWords = []
        foundWords.append(word + Constant.SUB_DELIMITER +
                          word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generate_card(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        card: Card = self.initialize_card(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        lacVietDict = LacVietDictionary()
        collinsDict = CollinsDictionary()

        # French to Vietnamese
        if translation.equals(Constant.FR_VN):

            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, card, lacVietDict)

        # French to English
        elif translation.equals(Constant.FR_EN):

            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, card, collinsDict)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target)

        return card
