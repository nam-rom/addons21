#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from .. enum.translation import Translation
from .. enum.card import Card
from .. enum.status import Status
from .. constant import Constant
from .. base_generator import BaseGenerator
from .. helpers.dict_helper import DictHelper

from .. dictionary.kantan import KantanDictionary
from .. dictionary.lacviet import LacVietDictionary


class VietnameseGenerator(BaseGenerator):

    def get_formatted_words(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        word = word.lower().strip()
        foundWords = []
        if translation.equals(Constant.VN_JP) and allWordTypes:
            foundWords += DictHelper.get_kantan_words(word)
        else:
            foundWords.append(word + Constant.SUB_DELIMITER +
                              word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generate_card(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        card: Card = self.initialize_card(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        lacVietDict = LacVietDictionary()
        kantan = KantanDictionary()

        # Vietnamese to English/French/Vietnamese
        if translation.equals(Constant.VN_EN) or translation.equals(Constant.VN_FR) or translation.equals(Constant.VN_VN):

            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, card, lacVietDict)

        # Vietnamese to Japanese
        elif translation.equals(Constant.VN_JP):

            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, card, kantan)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target)

        return card
