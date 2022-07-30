#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import urllib.parse

from typing import List
from bs4.element import Tag

from .. enum.meaning import Meaning
from .. enum.translation import Translation

from .. constant import Constant
from .. base_dictionary import BaseDictionary
from .. helpers.html_helper import HtmlHelper
from .. helpers.dict_helper import DictHelper


class KantanDictionary(BaseDictionary):

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

        urlParameters = "m=dictionary&fn=detail_word&id={}".format(self.wordId)
        self.doc = DictHelper.get_kantan_doc(
            Constant.KANTAN_URL_VN_JP_OR_JP_VN, urlParameters)
        logging.info("self.doc {}".format(self.doc))

        return True if not self.doc else False

    def is_invalid_word(self) -> bool:
        """Check if the input word exists in dictionary?"""

        mainWord = self.doc.select_one("#txtKanji")
        wordDetail = self.doc.select_one("#word-detail-info")

        return not mainWord and not wordDetail

    def get_word_type(self) -> str:
        if not self.wordType:
            element: Tag = HtmlHelper.get_doc_element(
                self.doc, "label[class*=word-type]", 0)
            self.wordType = "(" + element.get_text().strip() + \
                ")" if element else ""
        return self.wordType

    def get_example(self) -> str:
        examples = []
        exampleElms = []
        for i in range(4):
            example: str = HtmlHelper.get_doc_element(
                self.doc, "ul.ul-disc>li>u,ul.ul-disc>li>p", i)
            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example:
                break
            else:
                exampleElms.append(example)

        examples: list[str] = getKantanExamples(exampleElms)
        lowerWord = self.oriWord.lower()
        for i in range(len(examples)):
            example: str = examples[i].lower()
            if lowerWord in example:
                example = example.replace(
                    lowerWord, "{{c1::" + lowerWord + "}}")
            else:
                example = "{} {}".format(example, "{{c1::...}}")
            examples[i] = example

        return HtmlHelper.build_example(examples, True)

    def get_phonetic(self) -> str:
        if not self.phonetic:
            self.phonetic = HtmlHelper.get_text(self.doc, "span.romaji", 0)
        return self.phonetic

    def get_image(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        googleImage = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.oriWord)

        self.imageLink = HtmlHelper.get_attribute(
            self.doc, "a.fancybox.img", 0, "href")
        if not self.imageLink or "no-image" in self.imageLink:
            self.image = googleImage
            return self.image

        if "https" not in self.imageLink:
            self.imageLink = "https://kantan.vn" + self.imageLink
        self.imageLink = self.imageLink.replace("\\?w=.*$", "", 1)
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
            self.doc, "a.sound", 0, "data-fn")

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

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

        meanings: List[Meaning] = []

        # WordType
        meaning = Meaning()
        meanGroup: Tag = HtmlHelper.get_doc_element(
            self.doc, "#word-detail-info", 0)
        wordType: Tag = HtmlHelper.get_child_element(
            meanGroup, "label[class*=word-type]", 0)
        if wordType:
            meaning.wordType = wordType.get_text().strip().capitalize()
        meanings.append(meaning)

        # Meaning
        meanElms = meanGroup.select("ol.ol-decimal>li")
        for meanElm in meanElms:
            meaning = Meaning()
            mean: Tag = HtmlHelper.get_child_element(
                meanElm, ".nvmn-meaning", 0)
            if mean:
                meaning.meaning = mean.get_text()

            # Examples
            exampleElms = meanElm.select(
                "ul.ul-disc>li>u,ul.ul-disc>li>p")
            innerExamples: list[str] = getKantanExamples(exampleElms)
            if not innerExamples:
                meaning.examples = innerExamples
            meanings.append(meaning)

        # Kanji Meaning
        meaning = Meaning()
        kanji = HtmlHelper.get_child_outer_html(
            meanGroup, "#search-kanji-list", 0)
        if kanji:
            meaning.meaning = kanji.replace("\n", "")

        # Examples
        exampleElms = meanGroup.select(
            "#word-detail-info>ul.ul-disc>li>u,#word-detail-info>ul.ul-disc>li>p")
        examples = getKantanExamples(exampleElms)
        if examples:
            meaning.examples = examples
        meanings.append(meaning)

        return HtmlHelper.build_meaning(self.word, self.wordType, self.phonetic, meanings, True)

    def get_dictionary_name(self) -> str:
        return "Kantan Dictionary (Kantan.vn)"


def getKantanExamples(exampleElms: List[Tag]) -> List[str]:

    examples: List[str] = []
    if exampleElms:
        jpExamples: list[str] = []
        for exampleElem in exampleElms:
            if exampleElem.get("class"):
                examples.append(">>>>>" + exampleElem.get_text())
                jpExamples.append(exampleElem.get_text())
            else:
                examples.append(exampleElem.get_text())

        sentencesChain = "=>=>=>=>=>".join(jpExamples)
        sentencesChain = urllib.parse.quote(sentencesChain)

        urlParams = "m=dictionary&fn=furigana&keyword={}".format(
            sentencesChain)
        doc = DictHelper.get_kantan_doc(
            Constant.KANTAN_URL_VN_JP_OR_JP_VN, urlParams)
        sentencesChain = str(doc).replace("\n", "") if doc else sentencesChain
        jpExamples = sentencesChain.split("=&gt;=&gt;=&gt;=&gt;=&gt;")

        index = 0
        for i in range(len(examples)):
            if ">>>>>" in examples[i] and index < len(jpExamples):
                examples[i] = jpExamples[index]
                index = index + 1
    return examples
