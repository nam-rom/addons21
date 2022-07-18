"""
Motivanki Add-on for Anki
Copyright (c): 2020 The AnKing


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import random
from pathlib import Path

from aqt import mw
from aqt.gui_hooks import deck_browser_will_render_content

from .config import gc

ADDON_DIR_PATH = Path(__file__).parent


def add_new_count_to_bottom(dbinstance, content):
    COLOR = gc("font color", "Red")
    FAMILY = gc("font family", "Times")
    SIZE = gc("font size", "12px")
    QUOTE_LIST = gc("quote")
    QUOTE = random.choice(QUOTE_LIST)
    add_this = f"""<div style='color:{COLOR}; font-size:{SIZE}; font-family:{FAMILY};'>
    <br>{QUOTE}<br></div>"""
    content.stats += add_this


deck_browser_will_render_content.append(add_new_count_to_bottom)


# reset background when changing config
def apply_config_changes(config):
    mw.moveToState("deckBrowser")
    # mw.toolbar.draw()


mw.addonManager.setConfigUpdatedAction(__name__, apply_config_changes)


# needed so that it works if installed from AnkiWeb or not
def generate_config_md_from_template():
    with open(ADDON_DIR_PATH / "config_template.md", "r") as f:
        template = f.read()

    result = template.replace("ADDON_DIR_NAME", ADDON_DIR_PATH.name)

    with open(ADDON_DIR_PATH / "config.md", "w") as f:
        f.write(result)


generate_config_md_from_template()
