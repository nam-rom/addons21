# -*- coding: utf-8 -*-

from aqt import mw
from aqt.main import AnkiQt
from aqt.qt import Qt, QAction
from aqt.reviewer import Reviewer
from anki.hooks import wrap

AnkiQt._reviewState = wrap(
    AnkiQt._reviewState, lambda *_: mw.toolbar.web.hide(), "after")
AnkiQt.moveToState = wrap(
    AnkiQt.moveToState, lambda *_: mw.toolbar.web.show(), "before")

Reviewer._initWeb = wrap(
    Reviewer._initWeb, lambda _: mw.reviewer.bottom.web.eval(
        f"$('head').append(`<style>#outer {{ display: none }}</style>`)"))


