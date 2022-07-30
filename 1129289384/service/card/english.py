#!/usr/bin/python
# -*- coding: utf-8 -*-


from typing import List

from .. enum.translation import Translation
from .. enum.card import Card
from .. enum.status import Status
from .. constant import Constant
from .. base_generator import BaseGenerator
from .. helpers.dict_helper import DictHelper

from .. dictionary.lacviet import LacVietDictionary
from .. dictionary.cambridge import CambridgeDictionary
from .. dictionary.oxford import OxfordDictionary


class EnglishGenerator(BaseGenerator):

    def get_formatted_words(self, word: str, translation: Translation, allWordTypes: bool) -> List[str]:
        word = word.lower().strip()
        foundWords = []
        if translation.equals(Constant.EN_EN) and allWordTypes:
            foundWords += DictHelper.get_oxford_words(word)
        else:
            foundWords.append(word + Constant.SUB_DELIMITER +
                              word + Constant.SUB_DELIMITER + word)
        return foundWords

    def generate_card(self, formattedWord: str, ankiDir: str, translation: Translation, isOnline: bool) -> Card:

        formattedWord = formattedWord.lower()
        card: Card = self.initialize_card(formattedWord, translation)
        card.status = Status.SUCCESS
        card.comment = Constant.SUCCESS

        oxfordDict = OxfordDictionary()
        cambridgeDict = CambridgeDictionary()
        lacVietDict = LacVietDictionary()

        # English to English
        if (translation.equals(Constant.EN_EN)):

            card = self.single_dictionary_card(
                formattedWord, translation, ankiDir, isOnline, card, oxfordDict)

        # English to Chinese/French/Japanese
        elif translation.equals(Constant.EN_CN_TD) or translation.equals(Constant.EN_CN_SP) or translation.equals(Constant.EN_JP) or translation.equals(Constant.EN_FR):

            card = self.multiple_dictionaries_card(
                formattedWord, translation, ankiDir, isOnline, card, oxfordDict, cambridgeDict)

        # English to Vietnamese
        elif translation.equals(Constant.EN_VN):

            card = self.multiple_dictionaries_card(
                formattedWord, translation, ankiDir, isOnline, card, oxfordDict, lacVietDict)

        else:
            card.status = Status.NOT_SUPPORTED_TRANSLATION
            card.comment = Constant.NOT_SUPPORTED_TRANSLATION.format(
                translation.source, translation.target)

        return card
