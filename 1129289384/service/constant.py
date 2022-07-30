#!/usr/bin/python
# -*- coding: utf-8 -*-

from . enum.translation import Translation


class Constant:
    """Store all constant values for AnkiFlash"""

    # ANKI
    ANKI_DECK = "anki_deck.csv"

    # OXFORD
    OXFORD_SPELLING_WRONG = "Did you spell it correctly?"
    OXFORD_WORD_NOT_FOUND = "Oxford Learner's Dictionaries | Find the meanings"
    OXFORD_URL_EN_EN = "https://www.oxfordlearnersdictionaries.com/definition/english/{}"
    OXFORD_SEARCH_URL_EN_EN = "https://www.oxfordlearnersdictionaries.com/search/english/direct/?q={}"

    # LACVIET
    LACVIET_SPELLING_WRONG = "Dữ liệu đang được cập nhật"
    LACVIET_URL_VN_EN = "http://tratu.coviet.vn/tu-dien-lac-viet.aspx?learn=hoc-tieng-anh&t=V-A&k={}"
    LACVIET_URL_VN_FR = "http://tratu.coviet.vn/tu-dien-lac-viet.aspx?learn=hoc-tieng-phap&t=V-F&k={}"
    LACVIET_URL_VN_VN = "http://tratu.coviet.vn/tu-dien-lac-viet.aspx?learn=hoc-tieng-phap&t=V-V&k={}"
    LACVIET_URL_EN_VN = "http://tratu.coviet.vn/tu-dien-lac-viet.aspx?learn=hoc-tieng-anh&t=A-V&k={}"
    LACVIET_URL_FR_VN = "http://tratu.coviet.vn/tu-dien-lac-viet.aspx?learn=hoc-tieng-phap&t=F-V&k={}"

    # CAMBRIDGE
    CAMBRIDGE_SPELLING_WRONG = "Did you spell it correctly?"
    CAMBRIDGE_URL_EN_CN_TD = "https://dictionary.cambridge.org/search/english-chinese-traditional/direct/?q={}"
    CAMBRIDGE_URL_EN_CN_SP = "https://dictionary.cambridge.org/search/english-chinese-simplified/direct/?q={}"
    CAMBRIDGE_URL_EN_FR = "https://dictionary.cambridge.org/search/english-french/direct/?q={}"
    CAMBRIDGE_URL_EN_JP = "https://dictionary.cambridge.org/search/english-japanese/direct/?q={}"

    # COLLINS
    COLLINS_SPELLING_WRONG = "Sorry, no results for"
    COLLINS_URL_FR_EN = "https://www.collinsdictionary.com/search/?dictCode=french-english&q={}"

    # KANTAN
    KANTAN_URL_VN_JP_OR_JP_VN = "https://kantan.vn/postrequest.ashx"

    # JISHO
    JISHO_WORD_NOT_FOUND = "Sorry, couldn't find anything matching"
    JISHO_WORD_URL_JP_EN = "https://jisho.org/word/{}"
    JISHO_SEARCH_URL_JP_EN = "https://jisho.org/search/{}"

    # WORD REFERENCE
    WORD_REFERENCE_SPELLING_WRONG = ""
    WORD_REFERENCE_URL_EN_SP = ""
    WORD_REFERENCE_URL_SP_EN = ""

    # CONSTANTS
    TAB = "\t"
    MAIN_DELIMITER = "\\*\\*\\*"
    SUB_DELIMITER = "==="
    NO_EXAMPLE = "No example {{c1::...}}"
    SUCCESS = "Success"
    COPYRIGHT = "This card's content is collected from the following dictionaries: {}"
    WORD_NOT_FOUND = "Word not found. Could you please check spelling or feedback to us!"
    CONNECTION_FAILED = "Cannot connect to dictionaries, please try again later!"
    NOT_SUPPORTED_TRANSLATION = "The translation from {} to {} is not supported!"

    # LANGUAGES
    ENGLISH = "English"
    FRENCH = "French"
    VIETNAMESE = "Vietnamese"
    CHINESE = "Chinese"
    CHINESE_TD = "Chinese (Traditional)"
    CHINESE_SP = "Chinese (Simplified)"
    JAPANESE = "Japanese"
    SPANISH = "Spanish"

    # TRANSLATION
    EN_EN = Translation(ENGLISH, ENGLISH)
    EN_VN = Translation(ENGLISH, VIETNAMESE)
    EN_CN_TD = Translation(ENGLISH, CHINESE_TD)
    EN_CN_SP = Translation(ENGLISH, CHINESE_SP)
    EN_FR = Translation(ENGLISH, FRENCH)
    EN_JP = Translation(ENGLISH, JAPANESE)

    VN_EN = Translation(VIETNAMESE, ENGLISH)
    VN_FR = Translation(VIETNAMESE, FRENCH)
    VN_JP = Translation(VIETNAMESE, JAPANESE)
    VN_VN = Translation(VIETNAMESE, VIETNAMESE)

    FR_VN = Translation(FRENCH, VIETNAMESE)
    FR_EN = Translation(FRENCH, ENGLISH)

    JP_EN = Translation(JAPANESE, ENGLISH)
    JP_VN = Translation(JAPANESE, VIETNAMESE)
