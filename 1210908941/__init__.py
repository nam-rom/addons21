# Copyright: ijgnd
#            The AnKing
# Code License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Background images  were obtained from Pexels.com under this license https://www.pexels.com/photo-license/
# Gear icons were obtained from Wikimedia Commons https://commons.wikimedia.org/wiki/Category:Noto_Color_Emoji_Pie (license listed in link)

import os
import random
from typing import List

from anki import version as anki_version  # type: ignore
from anki.utils import pointVersion
from aqt import gui_hooks, mw
from aqt.addons import *
from aqt.editor import pics
# for the toolbar buttons
from aqt.qt import *

from .adjust_css_files22 import *
from .config import addon_path, addonfoldername, gc
from .gui.resources import initialize_qt_resources
from .gui_updatemanager import setupMenu

css_folder_for_anki_version = {
    "22": "22",
    "23": "22",
    "24": "22",
    "25": "25",
    "26": "25",
    "27": "25",
    "28": "25",
    "29": "25",
    "30": "25",
    "31": "31",
    "32": "31",
    "33": "31",
    "34": "31",
    "35": "31",
    "36": "36",
    "37": "36",
    "38": "36",
    "39": "36",
    "40": "36",
    "41": "36",
    "42": "36",
    "43": "36",
    "44": "36",
    "45": "36",
    "46": "36",
}

version = pointVersion()
if int(version) in css_folder_for_anki_version:
    version_folder = css_folder_for_anki_version[str(version)]
else:  # for newer Anki versions try the latest version and hope for the best
    version_folder = css_folder_for_anki_version[
        max(css_folder_for_anki_version, key=int)
    ]

SOURCE_ABSOLUTE = os.path.join(addon_path, "sources", "css", version_folder)
WEB_ABSOLUTE = os.path.join(addon_path, "web", "css")
CSS_FILES_TO_REPLACE = [
    os.path.basename(f) for f in os.listdir(WEB_ABSOLUTE) if f.endswith(".css")
]
WEB_EXPORTS_REGEX = r"(user_files.*|web.*)"


def main():
    initialize_qt_resources()
    setupMenu()

    mw.addonManager.setWebExports(__name__, WEB_EXPORTS_REGEX)
    update_css_files()

    gui_hooks.state_did_change.append(maybe_update_css_files)
    gui_hooks.webview_will_set_content.append(include_css_files)
    gui_hooks.deck_browser_will_render_content.append(replace_gears)

    def on_config_update(config):
        update_css_files()
        mw.moveToState("deckBrowser")

    mw.addonManager.setConfigUpdatedAction(__name__, on_config_update)


def update_css_files():
    # combine template files with config and write into webexports folder
    change_copy = [
        os.path.basename(f) for f in os.listdir(SOURCE_ABSOLUTE) if f.endswith(".css")
    ]
    for file_name in change_copy:
        with open(os.path.join(SOURCE_ABSOLUTE, file_name)) as f:
            content = f.read()

        if version == 22:
            if file_name == "deckbrowser.css":
                content = adjust_deckbrowser_css22(content)
            if file_name == "toolbar.css" and gc("Toolbar image"):
                content = adjust_toolbar_css22(content)
            if file_name == "overview.css":
                content = adjust_overview_css22(content)
            if file_name == "toolbar-bottom.css" and gc("Toolbar image"):
                content = adjust_bottomtoolbar_css22(content)
            if file_name == "reviewer.css" and gc("Reviewer image"):
                content = adjust_reviewer_css22(content)
            if (
                file_name == "reviewer-bottom.css"
                and gc("Reviewer image")
                and gc("Toolbar image")
            ):
                content = adjust_reviewerbottom_css22(content)

        # for later versions: try the latest
        # this code will likely change when new Anki versions are released which might require
        # updates of this add-on.
        else:
            if file_name == "deckbrowser.css":
                content = adjust_deckbrowser_css22(content)
            if file_name == "toolbar.css" and gc("Toolbar image"):
                content = adjust_toolbar_css22(content)
            if file_name == "overview.css":
                content = adjust_overview_css22(content)
            if file_name == "toolbar-bottom.css" and gc("Toolbar image"):
                content = adjust_bottomtoolbar_css22(content)
            if file_name == "reviewer.css" and gc("Reviewer image"):
                content = adjust_reviewer_css22(content)
            if file_name == "reviewer-bottom.css":  # and gc("Reviewer image"):
                content = adjust_reviewerbottom_css22(content)

        with open(os.path.join(WEB_ABSOLUTE, file_name), "w") as f:
            f.write(content)


# reset background when refreshing page (for use with "random" setting)
def maybe_update_css_files(new_state, old_state):
    if new_state != "deckBrowser":
        return

    update_css_files()
    if not tuple(int(i) for i in anki_version.split(".")) < (2, 1, 27):
        mw.toolbar.redraw()


def maybe_adjust_file_name(file_name):
    if pointVersion() >= 36:
        file_name = file_name.lstrip("css/")
    return file_name


def include_css_files(web_content, context):
    new_css: List[str] = web_content.css[:]
    for idx, file_name in enumerate(web_content.css):
        file_name = maybe_adjust_file_name(file_name)
        if file_name in CSS_FILES_TO_REPLACE:
            new_css[idx] = f"/_addons/{addonfoldername}/web/css/{file_name}"
            new_css.append(
                f"/_addons/{addonfoldername}/user_files/css/custom_{file_name}"
            )
    web_content.css = new_css


def replace_gears(deck_browser, content):
    old = """<img src='/_anki/imgs/gears.svg'"""
    new = f"""<img src='/_addons/{addonfoldername}/user_files/gear/{get_gearfile()}'"""
    if gc("Image name for gear") != "gears.svg":
        content.tree = content.tree.replace(old, new)
    else:
        content.tree = content.tree.replace(old, old)


def get_gearfile():
    gear_abs = os.path.join(addon_path, "user_files", "gear")
    gear_list = [os.path.basename(f) for f in os.listdir(gear_abs) if f.endswith(pics)]
    val = gc("Image name for gear")
    if val and val.lower() == "random":
        return random.choice(gear_list)
    if val in gear_list:
        return val
    else:
        # if empty or illegal value try to use 'AnKing.png' to signal that an illegal values was
        # used AnKing's gears folder doesn't contain a file named "gears.svg"
        if "AnKing.png" in gear_list:
            return "AnKing.png"
        else:
            return ""


main()
