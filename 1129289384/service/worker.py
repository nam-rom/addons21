#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import logging

from typing import List

from PyQt5.QtCore import QObject, pyqtSignal

from . enum.translation import Translation
from . enum.status import Status
from . enum.card import Card

from . base_generator import BaseGenerator
from . constant import Constant

from . card.chinese import ChineseGenerator
from . card.vietnamese import VietnameseGenerator
from . card.spanish import SpanishGenerator
from . card.japanese import JapaneseGenerator
from . card.french import FrenchGenerator
from . card.english import EnglishGenerator


class Worker(QObject):

    # Create a worker class to run in background using QThread
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    cardStr = pyqtSignal(str)
    failureStr = pyqtSignal(str)

    def __init__(self, generator, words, translation, mediaDir, isOnline, allWordTypes, ankiCsvPath):
        super().__init__()

        self.delimiter: str = "==="
        self.formattedWords: List[str] = []
        self.cards: List[Card] = []

        self.generator: BaseGenerator = generator
        self.words: List[str] = words
        self.translation: Translation = translation
        self.mediaDir: str = mediaDir
        self.isOnline: bool = isOnline
        self.allWordTypes: bool = allWordTypes
        self.csvFilePath: str = ankiCsvPath

    def generate_cards_background(self) -> List[Card]:
        """Generate flashcards from input words"""

        total: int = 0
        proceeded: int = 0
        cardCount: int = 0
        failureCount: int = 0

        total = len(self.words)
        for value in self.words:

            # Return if thread is interrupted
            if self.thread().isInterruptionRequested():
                break

            self.formattedWords = self.generator.get_formatted_words(
                value, self.translation, self.allWordTypes)
            total += len(self.formattedWords) - 1

            if len(self.formattedWords) > 0:
                for formattedWord in self.formattedWords:

                    # Return if thread is interrupted
                    if self.thread().isInterruptionRequested():
                        break

                    logging.info("formattedWord = '{}'".format(formattedWord))
                    card = self.generator.generate_card(
                        formattedWord, self.mediaDir, self.translation, self.isOnline)
                    time.sleep(0.2)
                    proceeded = proceeded + 1
                    percent = (proceeded / total) * 100
                    self.progress.emit(int(percent))

                    if card.status == Status.SUCCESS:
                        cardCount += 1
                        self.cards.append(card)
                        self.cardStr.emit(card.meaning)
                    else:
                        failureCount += 1
                        self.failureStr.emit(
                            "{} -> {}".format(formattedWord.split(self.delimiter)[0], card.comment))
            else:
                failureCount += 1
                self.failureStr.emit(Constant.WORD_NOT_FOUND)

        cardLines: list[str] = []
        for card in self.cards:

            # Return if thread is interrupted
            if self.thread().isInterruptionRequested():
                return

            cardContent = "{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".format(
                card.word if self.translation.equals(
                    Constant.VN_JP) else card.oriWord,
                Constant.TAB,
                card.wordType,
                Constant.TAB,
                card.phonetic,
                Constant.TAB,
                card.example,
                Constant.TAB,
                card.sounds,
                Constant.TAB,
                card.image,
                Constant.TAB,
                card.meaning,
                Constant.TAB,
                card.copyright,
                Constant.TAB,
                card.tag + "\n")
            cardLines.append(cardContent)

        try:
            os.remove(self.csvFilePath)
        except OSError:
            logging.info("{} does not exist!".format(self.csvFilePath))
            pass

        with open(self.csvFilePath, 'w', encoding='utf-8') as file:
            file.writelines(cardLines)

        # Return if thread is interrupted
        if self.thread().isInterruptionRequested():
            return

        # Finished
        self.progress.emit(100)
        self.finished.emit()
        return self.cards

    @staticmethod
    def initialize_generator(translation: Translation):

        generator = None

        if translation.source == Constant.ENGLISH:
            generator = EnglishGenerator()
        elif translation.source == Constant.JAPANESE:
            generator = JapaneseGenerator()
        elif translation.source == Constant.VIETNAMESE:
            generator = VietnameseGenerator()
        elif translation.source == Constant.FRENCH:
            generator = FrenchGenerator()
        elif translation.source == Constant.SPANISH:
            generator = SpanishGenerator()
        elif Constant.CHINESE in translation.source:
            generator = ChineseGenerator()

        return generator
