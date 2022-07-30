#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from typing import List

from .. enum.meaning import Meaning
from .. enum.translation import Translation

from .. constant import Constant
from .. base_dictionary import BaseDictionary
from .. helpers.html_helper import HtmlHelper
from .. helpers.dict_helper import DictHelper


class OxfordDictionary(BaseDictionary):

    def __init__(self):
        super().__init__()

    def search(self, formattedWord: str, translation: Translation) -> bool:
        """Find input word from dictionary data"""

        wordParts = formattedWord.split(self.delimiter)
        if self.delimiter in formattedWord and len(wordParts) == 3:
            self.word = wordParts[0]
            self.wordId = wordParts[1]
            self.oriWord = wordParts[2]
        else:
            raise RuntimeError(
                "Incorrect word format: {}".format(formattedWord))

        url = HtmlHelper.lookup_url(Constant.OXFORD_URL_EN_EN, self.wordId)
        self.doc = HtmlHelper.get_document(url)

        return True if not self.doc else False

    def is_invalid_word(self) -> bool:
        """Check if the input word exists in dictionary?"""

        title = HtmlHelper.get_text(self.doc, "title", 0)
        if Constant.OXFORD_SPELLING_WRONG in title or Constant.OXFORD_WORD_NOT_FOUND in title:
            return True

        word = HtmlHelper.get_text(self.doc, ".headword", 0)
        return False if word else True

    def get_word_type(self) -> str:
        if not self.wordType:
            self.wordType = HtmlHelper.get_text(self.doc, "span.pos", 0)
            self.wordType = "(" + self.wordType + ")" if self.wordType else ""
        return self.wordType

    def get_example(self) -> str:
        examples: list[str] = []
        for i in range(4):
            example: str = HtmlHelper.get_text(self.doc, "span.x", i)
            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example or example is None:
                break
            else:
                self.word = self.word.lower()
                example = example.lower()
                if self.word in example:
                    example = example.replace(
                        self.word, "{{c1::" + self.word + "}}")
                else:
                    # Anki will not hide the word, if we don't have "{{c1::...}}" for all examples!
                    example = "{} {}".format(example, "{{c1::...}}")
                examples.append(example)

        logging.info("examples: {}".format(examples))
        return HtmlHelper.build_example(examples)

    def get_phonetic(self) -> str:
        if not self.phonetic:
            phoneticBrE = HtmlHelper.get_text(self.doc, "span.phon", 0)
            phoneticNAmE = HtmlHelper.get_text(self.doc, "span.phon", 1)
            self.phonetic = "{} {}".format(
                phoneticBrE, phoneticNAmE).replace("//", " / ")
        return self.phonetic

    def get_image(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        googleImage = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.oriWord)

        self.imageLink = HtmlHelper.get_attribute(
            self.doc, "a.topic", 0, "href")

        if not self.imageLink:
            self.image = googleImage
            return self.image

        imageName = DictHelper.get_file_name(self.imageLink)
        if isOnline:
            self.image = "<img src=\"" + self.imageLink + "\"/>"
        else:
            self.image = "<img src=\"" + imageName + "\"/>"
            DictHelper.download_files(self.imageLink, False, ankiDir)
        return self.image

    def get_sounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = HtmlHelper.get_attribute(
            self.doc, "div.pron-uk", 0, "data-src-mp3")

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

        usSound = HtmlHelper.get_attribute(
            self.doc, "div.pron-us", 0, "data-src-mp3")
        if usSound:
            self.soundLinks = "{};{}".format(usSound, self.soundLinks)

        links = DictHelper.download_files(self.soundLinks, isOnline, ankiDir)
        for soundLink in links:
            soundName = DictHelper.get_file_name(soundLink)
            if isOnline:
                self.sounds = "<audio src=\"{}\" type=\"audio/wav\" preload=\"auto\" autobuffer controls>[sound:{}]</audio> {}".format(
                    soundLink, soundLink, self.sounds if len(self.sounds) > 0 else "")
            else:
                self.sounds = "<audio src=\"{}\" type=\"audio/wav\" preload=\"auto\" autobuffer controls>[sound:{}]</audio> {}".format(
                    soundName, soundName, self.sounds if len(self.sounds) > 0 else "")

        return self.sounds

    def get_meaning(self) -> str:
        self.get_word_type()
        self.get_phonetic()

        meanings: list[Meaning] = []

        # Word Form
        wordFormElm = self.doc.select_one("span.unbox[unbox=\"verbforms\"]")
        if wordFormElm:
            wordFormElms = wordFormElm.select("td.verbforms")
            wordForms = []
            for wordForm in wordFormElms:
                wordForms.append(wordForm.get_text().strip())

            meaning = Meaning("", wordForms)
            meaning.wordType = "Verb forms"
            meanings.append(meaning)

        meanGroups = self.doc.select(".sense")
        for meanElem in meanGroups:
            defElm = meanElem.select_one(".def")

            # See Also
            examples = []
            subDefElm = meanElem.select_one(".xrefs")
            if subDefElm:
                subDefPrefix = subDefElm.select_one(".prefix")
                subDefLink = subDefElm.select_one(".Ref")
                if subDefPrefix and subDefLink and "full entry" in subDefLink.get("title"):
                    examples.append("<a href=\"{}\">{} {}</a>".format(subDefLink.get(
                        "href"), subDefPrefix.get_text().strip().upper(), subDefLink.get_text().strip()))

            # Examples
            exampleElms = meanElem.select(".x")
            for exampleElem in exampleElms:
                examples.append(exampleElem.get_text().strip())
            meanings.append(
                Meaning(defElm.get_text().strip() if defElm else "", examples))

            # Extra Examples
            extraExample = HtmlHelper.get_child_element(
                meanElem, "span.unbox[unbox=\"extra_examples\"]", 0)
            if extraExample:
                exampleElms = extraExample.select(".unx")

                examples = []
                for exampleElm in exampleElms:
                    examples.append(exampleElm.get_text().strip())

                meaning = Meaning("", examples)
                meanings.append(meaning)

        # Word Family
        wordFamilyElm = self.doc.select_one("span.unbox[unbox=\"wordfamily\"]")
        if wordFamilyElm:
            wordFamilyElms = wordFamilyElm.select("span.p")

            wordFamilies = []
            for wordFamily in wordFamilyElms:
                wordFamilies.append(wordFamily.get_text().strip())

            meaning = Meaning("", wordFamilies)
            meaning.wordType = "Word family"
            meanings.append(meaning)

        return HtmlHelper.build_meaning(self.oriWord, self.wordType, self.phonetic, meanings)

    def get_dictionary_name(self) -> str:
        return "Oxford Advanced Learner's Dictionary"
