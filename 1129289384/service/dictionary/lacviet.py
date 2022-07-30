#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from .. enum.meaning import Meaning
from .. enum.translation import Translation

from .. constant import Constant
from .. base_dictionary import BaseDictionary
from .. helpers.html_helper import HtmlHelper
from .. helpers.dict_helper import DictHelper


class LacVietDictionary(BaseDictionary):

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

        url = ""
        if translation.equals(Constant.VN_EN):
            url = HtmlHelper.lookup_url(
                Constant.LACVIET_URL_VN_EN, self.wordId)
        elif (translation.equals(Constant.VN_FR)):
            url = HtmlHelper.lookup_url(
                Constant.LACVIET_URL_VN_FR, self.wordId)
        elif (translation.equals(Constant.VN_VN)):
            url = HtmlHelper.lookup_url(
                Constant.LACVIET_URL_VN_VN, self.wordId)
        elif (translation.equals(Constant.EN_VN)):
            url = HtmlHelper.lookup_url(
                Constant.LACVIET_URL_EN_VN, self.wordId)
        elif (translation.equals(Constant.FR_VN)):
            url = HtmlHelper.lookup_url(
                Constant.LACVIET_URL_FR_VN, self.wordId)

        self.doc = HtmlHelper.get_document(url)

        return True if not self.doc else False

    def is_invalid_word(self) -> bool:
        """Check if the input word exists in dictionary?"""

        words = self.doc.select("div.w.fl")
        if not words:
            return True

        warning = HtmlHelper.get_text(self.doc, "div.i.p10", 0)
        return Constant.LACVIET_SPELLING_WRONG in warning

    def get_word_type(self) -> str:
        if not self.wordType:
            element = HtmlHelper.get_doc_element(self.doc, "div.m5t.p10lr", 0)
            self.wordType = element.text.replace("|Tất cả", "").replace(
                "|Từ liên quan", "") if element else ""
            self.wordType = " | ".join(self.wordType.split("|"))

            if not self.wordType:
                elements = HtmlHelper.get_texts(self.doc, "div.m5t.p10lr")
                self.wordType = " | ".join(elements) if len(
                    elements) > 0 else ""

            self.wordType = "(" + self.wordType + ")" if self.wordType else ""
        return self.wordType

    def get_example(self) -> str:
        examples = []
        for i in range(4):
            example: str = HtmlHelper.get_text(self.doc, "div.e", i)
            if not example and i == 0:
                return Constant.NO_EXAMPLE
            elif not example:
                break
            else:
                self.word = self.word.lower()
                example = example.lower()
                if self.word in example:
                    example = example.replace(
                        self.word, "{{c1::" + self.word + "}}")
                else:
                    example = "{} {}".format(example, "{{c1::...}}")
                examples.append(example)

        return HtmlHelper.build_example(examples)

    def get_phonetic(self) -> str:
        if not self.phonetic:
            self.phonetic = HtmlHelper.get_text(self.doc, "div.p5l.fl.cB", 0)
        return self.phonetic

    def get_image(self, ankiDir: str, isOnline: bool) -> str:
        self.ankiDir = ankiDir
        self.imageLink = ""
        self.image = "<a href=\"https://www.google.com/search?biw=1280&bih=661&tbm=isch&sa=1&q={}\" style=\"font-size: 15px; color: blue\">Search images by the word</a>".format(
            self.oriWord)
        return self.image

    def get_sounds(self, ankiDir: str, isOnline: bool) -> List[str]:
        self.ankiDir = ankiDir
        self.soundLinks = HtmlHelper.get_attribute(
            self.doc, "embed", 0, "flashvars")

        if not self.soundLinks:
            self.sounds = ""
            self.soundLinks = ""
            return self.sounds

        self.soundLinks = self.soundLinks.replace(
            "file=", "").replace("&autostart=false", "")

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
        meanGroups = self.doc.select("div[id*=partofspeech]")

        for meanGroup in meanGroups:
            if meanGroup.get("id").lower() != "partofspeech_100":
                meanElms: list = meanGroup.select("div")
                meanCount = len(meanGroup.select(".m"))

                meaning = Meaning()
                examples = []
                firstMeaning = True

                for meanElm in meanElms:
                    if meanElm.has_attr("class") and "ub" in meanElm.get("class"):
                        if meanCount > 0:
                            # has meaning -> get text
                            meaning.wordType = meanElm.get_text().strip().capitalize()
                        else:
                            # only type -> get inner html
                            meaning.wordType = meanElm.get_text().strip().replace("\n", "").capitalize()
                    elif meanElm.has_attr("class") and "m" in meanElm.get("class"):
                        # from the second meaning tag
                        if not firstMeaning:
                            meaning.examples = examples
                            meanings.append(meaning)
                            # reset value
                            meaning = Meaning()
                            examples = []
                        meaningTags = meanElm.select("a")
                        if len(meaningTags) > 0:
                            # add correct url prefix for all <a> tags
                            for aTag in meaningTags:
                                replaceTag = aTag
                                replaceTag["href"] = "http://tratu.coviet.vn/" + \
                                    aTag.get("href")
                                aTag.replaceWith(replaceTag)

                            meaning.meaning = str(meanElm).strip()
                        else:
                            meaning.meaning = meanElm.get_text().strip()
                        firstMeaning = False
                    elif meanElm.has_attr("class") and ("e" in meanElm.get("class") or "em" in meanElm.get("class") or "im" in meanElm.get("class") or "id" in meanElm.get("class") or "href" in meanElm.get("class")):
                        examples.append(meanElm.get_text().strip())

                meaning.examples = examples
                meanings.append(meaning)

        return HtmlHelper.build_meaning(self.oriWord, self.wordType, self.phonetic, meanings)

    def get_dictionary_name(self) -> str:
        return "Lac Viet Dictionary"
