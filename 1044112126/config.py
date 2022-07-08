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

from abc import ABC, abstractmethod
from collections import UserDict
from enum import Enum
from typing import TYPE_CHECKING

from PyQt5.QtCore import QObject, pyqtSignal

from .profile import ProfileAdapter

if TYPE_CHECKING:
    from aqt.addons import AddonManager


class HotkeySettingName(Enum):
    """
    The values of this enum are assumed to be kept in sync with:
    - config.json
    - widget names in settings.ui
    - signal names in hotkeys.py
    """

    OPEN_NEXT_POPUP = "hotkeyOpenNextPopup"
    OPEN_PREVIOUS_POPUP = "hotkeyOpenPreviousPopup"
    CLOSE_POPUP = "hotkeyClosePopup"
    TOGGLE_SIDE_PANEL = "hotkeyToggleSidePanel"


class DisplaySettingName(Enum):
    """
    The values of this enum are assumed to be kept in sync with:
    - config.json
    - widget names in settings.ui
    """

    ENABLE_GENERAL = "enablePopupDefinitions"
    ENABLE_QUESTION = "enablePopupDefinitonsOnQuestions"
    ENABLE_ARTICLE_VIEWER = "enableArticleViewer"


class ColorSettingName(Enum):
    """
    The values of this enum are assumed to be kept in sync with:
    - config.json
    - widget names in settings.ui
    """

    HIGHLIGHTS = "styleColorHighlights"


class ConfigError(Exception):
    pass


class ConfigSignals(QObject):
    saved = pyqtSignal()


class ConfigProvider(ABC):
    @abstractmethod
    def read(self) -> dict:
        pass

    @abstractmethod
    def write(self, data: dict):
        pass

    @abstractmethod
    def read_defaults(self) -> dict:
        pass


class AnkiJSONConfigProvider(ConfigProvider):
    def __init__(
        self,
        addon_package: str,
        addon_manager: "AddonManager",
    ):
        self._addon_package = addon_package
        self._addon_manager = addon_manager

    def read(self) -> dict:
        config = self._addon_manager.getConfig(self._addon_package)
        if config is None:
            # this should never happen, unless add-on files have been
            # tampered with
            raise ConfigError("Could not read add-on configuration")
        return config

    def write(self, data: dict):
        self._addon_manager.writeConfig(self._addon_package, data)

    def read_defaults(self) -> dict:
        defaults = self._addon_manager.addonConfigDefaults(self._addon_package)
        if defaults is None:
            # this should never happen, unless add-on files have been
            # tampered with
            raise ConfigError("Could not read add-on configuration defaults")
        return defaults


class AddonConfig(UserDict):
    def __init__(
        self,
        config_provider: ConfigProvider,
        config_signals: ConfigSignals,
        profile_adapter: ProfileAdapter,
    ):
        super().__init__()
        self._config_provider = config_provider
        self._profile_adapter = profile_adapter
        self.data = self._config_provider.read()
        self.signals = config_signals

    def save(self):
        self._config_provider.write(self.data)
        self.signals.saved.emit()

    def defaults(self) -> dict:
        return self._config_provider.read_defaults()
