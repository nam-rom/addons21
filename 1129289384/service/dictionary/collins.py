#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import List

from .. enum.meaning import Meaning
from .. enum.translation import Translation

from .. constant import Constant
from .. base_dictionary import BaseDictionary
from .. helpers.html_helper import HtmlHelper
from .. helpers.dict_helper import DictHelper


class CollinsDictionary(BaseDictionary):

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

        url = HtmlHelper.lookup_url(Constant.COLLINS_URL_FR_EN, self.wordId)
        self.doc = HtmlHelper.get_document(url)

        return True if not self.doc else False

    def is_invalid_word(self) -> bool:
        """Check if the input word exists in dictionary?"""

        mainContent = HtmlHelper.get_text(self.doc, "div.content-box", 0)
        if Constant.COLLINS_SPELLING_WRONG in mainContent:
            return True

        self.word = HtmlHelper.get_text(self.doc, "h2.h2_entry>span", 0)
        return not self.word

    def get_word_type(self) -> str:
        if not self.wordType:
            texts = HtmlHelper.get_texts(self.doc, "span.pos")
            self.wordType = "(" + " / ".join(texts) + \
                ")" if len(texts) > 0 else ""
        return self.wordType

    def get_example(self) -> str:
        examples = []
        for i in range(4):
            example: str = HtmlHelper.get_text(
                self.doc, ".re.type-phr,.cit.type-example", i)
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
            self.phonetic = HtmlHelper.get_text(self.doc, "span.pron.type-", 0)
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
            self.doc, "a.hwd_sound.sound.audio_play_button.icon-volume-up.ptr", 0, "data-src-mp3")

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
        meanElms = self.doc.select("div.hom")
        for meanElm in meanElms:
            meaning = Meaning()
            # WordType
            wordType = HtmlHelper.get_child_element(meanElm, "span.pos", 0)
            meaning.wordType = wordType.get_text().capitalize() if wordType else ""

            # Meaning
            means = meanElm.select("div.sense")
            for mean in means:
                re = mean.select_one("span[class*=sensenum]")
                if re:
                    re.decompose()
                meaning.meaning = str(mean).replace("\n", " ")
                meanings.append(meaning)
                meaning = Meaning()

        # Examples
        meaning = Meaning()
        examples = []
        examElms = self.doc.select("div.listExBlock .quote")
        for exam in examElms:
            examples.append(exam.get_text())
        meaning.examples = examples
        meaning.wordType = "Extra examples"
        meanings.append(meaning)

        return HtmlHelper.build_meaning(self.word, self.wordType, self.phonetic, meanings)

    def get_dictionary_name(self) -> str:
        return "Collins Dictionary"
