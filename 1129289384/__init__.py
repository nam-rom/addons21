#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
AnkiFlash Importer

This is the next generation of AnkiFlash Importer, it's now not only include importer but also embeded the generator inside.
* Generator helps you to generate flashcards for learning vocabularies
* Importer helps to import those flashcards into Anki

Author: Long Ly
Website: https://www.facebook.com/ankiflashcom
Modified: Jun 24, 2021
"""

from aqt import mw
from PyQt5.QtWidgets import QAction

from os.path import join
from logging.handlers import RotatingFileHandler

from . service.constant import Constant
from . ui.generator_dialog import GeneratorDialog

import os
import logging

version = '1.1.0'


class AnkiFlash():
    """AnkiFlash"""

    def __init__(self, version):

        # disable old log process
        logging.shutdown()

        # Directories
        self.addonDir = join(mw.pm.addonFolder(), "1129289384")
        self.mediaDir = mw.col.media.dir()
        os.makedirs(self.mediaDir, exist_ok=True)

        # Paths
        self.iconPath = join(self.addonDir, r'resources/anki.png')
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)

        # Config Logging (Rotate Every 10MB)
        os.makedirs(join(self.addonDir, r'logs'), exist_ok=True)
        self.ankiFlashLog = join(self.addonDir, r'logs/ankiflash.log')

        rfh = RotatingFileHandler(
            filename=self.ankiFlashLog, maxBytes=50000000, backupCount=3, encoding='utf-8')
        should_roll_over = os.path.isfile(self.ankiFlashLog)
        if should_roll_over:
            rfh.doRollover()
        logging.basicConfig(level=logging.INFO,
                            format=u"%(asctime)s - %(threadName)s [%(thread)d] - %(message)s",
                            datefmt="%d-%b-%y %H:%M:%S",
                            handlers=[rfh])

        # Create Generator Dialog
        self.generator = GeneratorDialog(
            version, self.iconPath, self.addonDir, self.mediaDir)
        self.generator.show()


def ankiFlash():
    mw.ankiFlash = AnkiFlash(version)


ankiFlashAct = QAction("AnkiFlash {}".format(version), mw)
ankiFlashAct.triggered.connect(ankiFlash)
mw.form.menuTools.addAction(ankiFlashAct)
