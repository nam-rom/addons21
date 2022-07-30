#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from aqt import mw
from anki.models import ModelManager
from anki.importing.csvfile import TextImporter

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from shutil import copyfile

from . ui_importer import UiImporter
from .. service.constant import Constant
from .. service.helpers.anki_helper import AnkiHelper

from os.path import join

import logging
import csv
csv.field_size_limit(2**30)


class ImporterDialog(QDialog):

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, version, iconPath, addonDir, mediaDir):

        super().__init__()
        self.version = version
        self.addonDir = addonDir
        self.mediaDir = mediaDir
        self.iconPath = iconPath

        # Paths
        self.ankiCsvPath = join(self.addonDir, Constant.ANKI_DECK)
        self.frontFile = join(self.addonDir, r'resources/front.html')
        self.backFile = join(self.addonDir, r'resources/back.html')
        self.cssFile = join(self.addonDir, r'resources/style.css')

        # Importer GUI
        self.ui = UiImporter()
        self.ui.setupUi(self, version, iconPath)

        # Check if Import button should be enabled or disabled
        self.ui.deckNameTxt.textChanged.connect(self.enable_import_btn)

        # Handle Import button clicked
        self.ui.importBtn.clicked.connect(
            lambda: self.btn_import_clicked(version))

    def key_press_event(self, event):
        super().key_press_event(event)
        self.keyPressed.emit(event.key())

    def on_key(self, key):
        if key == QtCore.Qt.Key_Return and self.ui.deckNameTxt.text():
            self.btn_import_clicked(self.version)
        else:
            logging.info('key pressed: {}'.format(key))

    def enable_import_btn(self):
        if self.ui.deckNameTxt.text():
            self.ui.importBtn.setEnabled(True)
        else:
            self.ui.importBtn.setEnabled(False)

    def btn_import_clicked(self, version):
        self.ui.importProgressBar.setValue(20)

        with open(self.frontFile, 'r', encoding='utf-8') as file:
            self.front = file.read()

        with open(self.backFile, 'r', encoding='utf-8') as file:
            self.back = file.read()

        with open(self.cssFile, 'r', encoding='utf-8') as file:
            self.css = file.read()

        updateExistingNote = self.ui.checkBox.isChecked()
        # Create note type if needs
        noteTypeName = u'AnkiFlashTemplate.{}'.format(version)
        is_note_type_diff = self.is_note_type_diff(
            noteTypeName, self.front, self.back, self.css)

        # Create new note type if not exist or existent but won't to update existing!
        if (is_note_type_diff == None) or (is_note_type_diff != None and not updateExistingNote):
            # If note type already existed, and we don't want to udpate existing! We need a new name!
            if is_note_type_diff != None:
                noteTypeName = u'AnkiFlashTemplate.{}.{}'.format(
                    version, AnkiHelper.id_generator())
                noteTypeId = mw.col.models.id_for_name(noteTypeName)
                while (noteTypeId != None):
                    noteTypeName = u'AnkiFlashTemplate.{}.{}'.format(
                        version, AnkiHelper.id_generator())
                    noteTypeId = mw.col.models.id_for_name(noteTypeName)

            self.create_note_type(
                noteTypeName, self.front, self.back, self.css)
            logging.info("{} Note type created.".format(noteTypeName))

        elif is_note_type_diff and updateExistingNote:
            self.update_note_type(
                noteTypeName, self.front, self.back, self.css)
            logging.info(
                "{} Note type is existent, override it.".format(noteTypeName))
        else:
            logging.info(
                "{} Note type is existent, the same with AnkiFlash, use it.".format(noteTypeName))
        self.ui.importProgressBar.setValue(50)

        # Import csv text file into Anki
        self.import_text_file(self.ui.deckNameTxt.text(),
                              noteTypeName, self.ankiCsvPath)
        self.ui.importProgressBar.setValue(100)
        logging.info("Imported csv file: {}".format(self.ankiCsvPath))

        AnkiHelper.message_box("Info",
                               "Finished importing flashcards.",
                               "Let's enjoy learning curve.",
                               self.iconPath)

        os.makedirs(join(self.mediaDir, r'resources'), exist_ok=True)
        copyfile(join(self.addonDir, r'resources/Raleway-Regular.ttf'),
                 join(self.mediaDir, r'resources/Raleway-Regular.ttf'))
        copyfile(join(self.addonDir, r'resources/OpenSans-Regular.ttf'),
                 join(self.mediaDir, r'resources/OpenSans-Regular.ttf'))

        self.close()

    def is_note_type_diff(self, noteTypeName, front, back, css):
        # Get note type
        noteType = mw.col.models.byName(noteTypeName)
        if noteType == None:
            return None

        # Get template
        tempates = noteType["tmpls"]
        for temp in tempates:
            if temp["name"] == "AnkiFlash":
                template = temp

        # Compare question
        asIsFrontMd5 = AnkiHelper.md5_utf8(template["qfmt"])
        toBeFrontMd5 = AnkiHelper.md5_utf8(front)
        if(asIsFrontMd5 != toBeFrontMd5):
            return True

        # Compare answers
        asIsBackMd5 = AnkiHelper.md5_utf8(template["afmt"])
        toBeBackMd5 = AnkiHelper.md5_utf8(back)
        if(asIsBackMd5 != toBeBackMd5):
            return True

        # Compate css
        asIsCssMd5 = AnkiHelper.md5_utf8(noteType["css"])
        toBeCssMd5 = AnkiHelper.md5_utf8(css)
        if(asIsCssMd5 != toBeCssMd5):
            return True

        return False

    def create_note_type(self, noteTypeName, front, back, css):
        # Create empty note type
        mm = ModelManager(mw.col)
        nt = mm.new(noteTypeName)

        # Add fields into note type
        mm.add_field(nt, mm.new_field("Word"))
        mm.add_field(nt, mm.new_field("WordType"))
        mm.add_field(nt, mm.new_field("Phonetic"))
        mm.add_field(nt, mm.new_field("Example"))
        mm.add_field(nt, mm.new_field("Sound"))
        mm.add_field(nt, mm.new_field("Image"))
        mm.add_field(nt, mm.new_field("Content"))
        mm.add_field(nt, mm.new_field("Copyright"))

        # Add template into note type
        template = mm.new_template("AnkiFlash")
        template["qfmt"] = front
        template["afmt"] = back
        nt["css"] = css
        mm.add_template(nt, template)

        # Save model / note type
        mm.save(nt)

        # Update UI
        mw.reset()

    def update_note_type(self, noteTypeName, front, back, css):

        noteType = mw.col.models.byName(noteTypeName)
        if noteType == None:
            raise RuntimeError(
                "{} Note type not found!".format(noteTypeName))

        # Get template
        tempates = noteType["tmpls"]
        for temp in tempates:
            if temp["name"] == "AnkiFlash":
                template = temp

        # Add template into note type
        template["qfmt"] = front
        template["afmt"] = back
        noteType["css"] = css

        # Save model / note type
        mm = ModelManager(mw.col)
        mm.save(noteType)

        # Update UI
        mw.reset()

    def import_text_file(self, deckName, noteTypeName, csvPath):
        # Select deck
        did = mw.col.decks.id(deckName)
        mw.col.decks.select(did)

        # Set note type for deck
        m = mw.col.models.by_name(noteTypeName)
        deck = mw.col.decks.get(did)
        deck["mid"] = m["id"]
        mw.col.decks.save(deck)

        # Import into the collection
        ti = TextImporter(mw.col, csvPath)
        ti.model["id"] = m["id"]

        mw.col.set_aux_notetype_config(
            ti.model["id"], "lastDeck", did
        )
        mw.col.models.save(ti.model, updateReqs=False)

        # ADD_MODE: import even if first field matches existing note
        ti.importMode = 2
        ti.delimiter = "\t"
        ti.allowHTML = True
        ti.open()
        ti.updateDelimiter()
        ti.run()

        # Update UI
        mw.reset()
