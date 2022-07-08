# AMBOSS Anki Add-on
#
# Copyright (C) 2019-2020 AMBOSS MD Inc. <https://www.amboss.com/us>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
from typing import Callable

from aqt.utils import openLink

from .auth import AuthDialog, LoginHandler, RegisterHandler
from .debug import ErrorPromptFactory
from .links import ExternalLinkHandler
from .reviewer import ReviewerTooltipUpdater
from .shared import _

AMBOSS_LINK_PREFIX = "amboss"


class ReviewerBridge:
    """Handles hijacked AMBOSS specific Anki reviewer bridge links."""

    def __init__(
        self,
        reviewer_tooltip_updater: ReviewerTooltipUpdater,
        external_link_handler: ExternalLinkHandler,
    ):

        self._reviewer_tooltip_updater = reviewer_tooltip_updater
        self._external_link_handler = external_link_handler

    def __call__(self, cmd, payload):
        if cmd == "tooltip":
            payload = json.loads(payload)
            self._reviewer_tooltip_updater.update_tooltip(payload)
        elif cmd == "url":
            self._external_link_handler.open_url(payload)
        elif cmd == "isArticleViewerInternal":
            return self._external_link_handler.is_article_viewer_internal()


class AuthBridge:
    """Handles all auth bridge links."""

    def __init__(
        self,
        login_handler: LoginHandler,
        register_handler: RegisterHandler,
        auth_dialog: AuthDialog,
        on_dom_done: Callable,
    ):
        self._login_handler = login_handler
        self._register_handler = register_handler
        self._auth_dialog = auth_dialog
        self._on_dom_done = on_dom_done

    def __call__(self, url, *args):
        if url.lower().startswith("http"):
            return openLink(url)
        elif url == "domDone":
            self._on_dom_done()
            return False
        elif not url.startswith(AMBOSS_LINK_PREFIX):
            return True
        _, cmd, *data = url.split(":")
        if cmd == "login" and len(data) >= 2:
            username, password = data[0], data[1]
            return self._login_handler.login(username, password)
        if cmd == "register" and len(data) >= 2:
            username, password, password_repeat = data[0], data[1], data[2]
            return self._register_handler.register(username, password, password_repeat)
        elif cmd == "close":
            self._auth_dialog.accept()
        return False


class AboutBridge:
    def __init__(self, error_prompt_factory: ErrorPromptFactory):
        self._error_prompt_factory = error_prompt_factory

    def __call__(self, url, *args):
        if url.lower().startswith("http"):
            return openLink(url)
        elif not url.startswith(AMBOSS_LINK_PREFIX):
            return True
        __, cmd, *args = url.split(":")
        if cmd == "debug":
            self._error_prompt_factory.create(
                None,
                _("Something isn't working like you expected?"),
                _("AMBOSS - Debug"),
            )
