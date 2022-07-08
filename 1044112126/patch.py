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
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, List, Tuple, Union

# keep this import, required in both current and legacy business logic
from aqt.reviewer import Reviewer

from .controller import CONTROLLER_PREFIX, Controller
from .hooks import profile_did_open
from .indicator import Indicator
from .reviewer import wrap
from .shared import safe_print

if TYPE_CHECKING:
    from aqt.toolbar import Toolbar  # type-hints only, separate import for legacy paths
    from aqt.toolbar import TopToolbar  # 2.1.22+
    from aqt.webview import WebContent  # 2.1.22+
else:
    # this weird pattern is needed for mypy to not complain while still being
    # able to evaluate TopToolbar outside of TYPE_CHECKING
    try:
        from aqt.toolbar import TopToolbar
    except (ImportError, ModuleNotFoundError):
        TopToolbar = None


class Patcher(ABC):
    @abstractmethod
    def patch(self):
        raise NotImplementedError


class ReviewerHookPatcher(Patcher):
    """
    Patches link handling to use our controller via hooks.
    Does only support Anki >= 2.1.22, preferred whenever available.
    """

    def __init__(self, controller: Controller):
        self._controller = controller

    def patch(self):
        from aqt.gui_hooks import webview_did_receive_js_message

        webview_did_receive_js_message.append(self._on_webview_did_receive_js_message)

    def _on_webview_did_receive_js_message(
        self, handled: Tuple[bool, Any], message: str, context: Any
    ) -> Tuple[bool, Any]:
        if not isinstance(context, Reviewer):
            return handled
        if not message.startswith(CONTROLLER_PREFIX):
            return handled
        return True, self._controller(message)


class ReviewerMonkeyPatcher(Patcher):
    """
    Monkey-patches the Reviewer._linkHandler method to do custom link handling
    Preferably used on Anki < 2.1.22 only, later versions support cleaner and less risky hooks.
    """

    def __init__(self, controller: Controller):
        self._controller = controller

    def patch(self):
        # NOTE: consider using anki.hooks.wrap instead
        Reviewer._linkHandler = wrap(
            Reviewer._linkHandler, ReviewerMonkeyPatcher._link_handler, self
        )

    def _link_handler(self, reviewer: Reviewer, link: str, _old: Callable):
        if not link.startswith(CONTROLLER_PREFIX):
            return _old(reviewer, link)
        return self._controller(link)


class TopToolbarHookPatcher(Patcher):
    def __init__(
        self,
        controller: Controller,
        package_name: str,
        indicator: Indicator,
        js: Tuple[str, ...] = (),
    ):
        self._controller = controller
        self._package_name = package_name
        self._indicator = indicator
        self._js = js

    def patch(self):
        from aqt.gui_hooks import (
            top_toolbar_did_init_links,
            webview_did_receive_js_message,
            webview_will_set_content,
        )

        webview_will_set_content.append(self._on_webview_will_set_content)
        webview_did_receive_js_message.append(self._on_webview_did_receive_js_message)
        top_toolbar_did_init_links.append(self._on_top_toolbar_did_init_links)

    def _on_webview_will_set_content(
        self, web_content: "WebContent", context: Union[Any, "TopToolbar"]
    ):
        if TopToolbar is None or not isinstance(context, TopToolbar):
            return

        web_content.js += [f"/_addons/{self._package_name}/web/{f}" for f in self._js]
        web_content.head += "\n".join(
            [
                f"<script>ambossAddon.indicator.toggle({json.dumps(self._indicator.show)});</script>"
            ]
        )
        web_content.css.append(f"/_addons/{self._package_name}/web/css/indicator.css")

    def _on_webview_did_receive_js_message(
        self, handled: Tuple[bool, Any], message: str, context: Any
    ) -> Tuple[bool, Any]:
        if not isinstance(context, TopToolbar):
            return handled
        if not message.startswith(CONTROLLER_PREFIX):
            return handled
        return True, self._controller(message)

    def _on_top_toolbar_did_init_links(self, links: List[str], *args):
        links.append(self._indicator.indicator_markup())


class TopToolbarMonkeyPatcher(Patcher):
    def __init__(
        self,
        controller: Controller,
        package_name: str,
        indicator: Indicator,
        js: Tuple[str, ...] = (),
    ):
        self._controller = controller
        self._package_name = package_name
        self._indicator = indicator
        self._js = js

    def patch(self):
        from anki.hooks import wrap as anki_wrap
        from aqt.toolbar import Toolbar

        Toolbar._linkHTML = anki_wrap(Toolbar._linkHTML, self._link_html, "around")  # type: ignore
        Toolbar._linkHandler = anki_wrap(  # type: ignore
            Toolbar._linkHandler, self._link_handler, "around"
        )
        self._indicator.toolbar_redraw()

    def _link_html(self, toolbar: "Toolbar", links: List[str], _old: Callable) -> str:
        return "\n".join(
            [
                f"""<script src="/_addons/{self._package_name}/web/{f}"></script>"""
                for f in self._js
            ]
            + [
                f"<script>ambossAddon.indicator.toggle({json.dumps(self._indicator.show)});</script>",
                _old(toolbar, links),
                f"""<link rel="stylesheet" href="/_addons/{self._package_name}/web/css/indicator.css">""",
                self._indicator.indicator_markup(),
            ]
        )

    def _link_handler(self, toolbar: "Toolbar", link: str, _old: Callable):
        if not link.startswith(CONTROLLER_PREFIX):
            return _old(toolbar, link)
        return self._controller(link)


class TopToolbar22Patcher(TopToolbarHookPatcher, TopToolbarMonkeyPatcher):
    """Supports Anki 2.1.22+. Uses hooks where applicable, monkey-patching where not."""

    def patch(self):
        from anki.hooks import wrap as anki_wrap
        from aqt.toolbar import Toolbar

        super().patch()
        Toolbar._linkHTML = anki_wrap(Toolbar._linkHTML, super()._link_html, "around")  # type: ignore


class MultiPatcher:
    """
    Patches Anki classes, e.g., to use our controller on Anki's python-javascript bridge.
    Forgivingly tries patch strategies in descending order until one works.
    """

    def __init__(self, *patch_strategies: Patcher):
        self._patch_strategies = patch_strategies
        self._patched: bool = False

    def defer_patch_once(self):
        """
        Defer patch until profile loaded to win out in possible add-on conflicts
        when using the monkey-patch strategy.
        """
        profile_did_open.append(self.patch_once)

    def patch_once(self):
        """
        Only fire on first profile load. Hook subscriptions persist across
        profile switches, so we do not want to repeat them on next profile load
        """
        if self._patched:
            return
        self._patch()
        self._patched = True

    def _patch(self):
        exc = None
        for patch_strategy in self._patch_strategies:
            try:
                patch_strategy.patch()
            except Exception as e:
                exc = e
            else:
                return
        if exc:
            raise exc


class ReviewerHTMLPatcher:
    """Injects our JS and CSS into reviewer web content."""

    def __init__(
        self,
        base_folder: str,
        js: Tuple[str, ...] = (),
        css: Tuple[str, ...] = (),
        css_calls: Tuple[Callable, ...] = (),
    ):

        self._base_folder = base_folder
        self._js = js
        self._css = css
        self._css_calls = css_calls

    def patch(self):
        """"""
        try:  # Anki 2.1.22+
            # register web content hook to update reviewer HTML content
            from aqt.gui_hooks import webview_will_set_content

            webview_will_set_content.append(self._on_webview_will_set_content)
        except (ImportError, ModuleNotFoundError):
            # Legacy: monkey-patch original Reviewer.revHtml method to add
            # our own web elements.
            # NOTE: consider using anki.hooks.wrap instead
            Reviewer.revHtml = wrap(
                Reviewer.revHtml, ReviewerHTMLPatcher._on_rev_html, self
            )

    def _on_webview_will_set_content(
        self, web_content: "WebContent", context: Reviewer
    ):
        if not isinstance(context, Reviewer):
            # TODO?: Extend support to other web views
            return

        web_content.body += self._injection()

    def _injection(self):
        inject = "\n"
        for f in self._js:
            inject += f"""<script src="{self._base_folder}/{f}"></script>\n"""
        for f in self._css:
            inject += f"""<link rel="stylesheet" href="{self._base_folder}/{f}">\n"""
        for c in self._css_calls:
            inject += f"<style>{c()}</style>\n"
        return inject

    def _on_rev_html(self, reviewer: Reviewer, _old: Callable):
        """
        :param reviewer: original Reviewer instance to be monkey-patched
        :param _old: original Reviewer.revHtml
        :return: reviewer HTML code
        """
        return _old(reviewer) + self._injection()


class AddonManagerUpdatePatcher(Patcher):
    """Monkey-patch aqt.addons.AddonManager to disable AnkiWeb-served updates"""

    def __init__(self, package_name: str):
        if not package_name.isdigit():
            raise ValueError("Provided package is not an ankiweb-managed add-on")
        self._package_name: str = package_name
        self._ankiweb_id: Union[str, int]

    def patch(self):
        from anki.hooks import wrap as anki_wrap
        from aqt.addons import AddonManager

        try:  # 2.1.20+
            AddonManager.updates_required = anki_wrap(
                AddonManager.updates_required, self._on_updates_required, "around"
            )
            # Modern Anki and legacy Anki use different types for add-on IDs
            self._ankiweb_id = int(self._package_name)
        except AttributeError:
            AddonManager._updatedIds = anki_wrap(  # type: ignore
                AddonManager._updatedIds,  # type: ignore
                self._on_updates_required,
                "around",
            )
            self._ankiweb_id = self._package_name

    def _on_updates_required(self, *args, _old: Callable, **kwargs):
        need_update: List[Union[int, str]] = _old(*args, **kwargs)

        if not isinstance(need_update, list) or (
            need_update and not isinstance(need_update[0], type(self._ankiweb_id))
        ):
            safe_print("Unexpected ankiweb update list data type")

        try:
            need_update.remove(self._ankiweb_id)
        except Exception:
            pass

        return need_update
