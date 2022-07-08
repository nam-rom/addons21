# AMBOSS Anki Add-on
#
# Copyright (C) 2019-2021 AMBOSS MD Inc. <https://www.amboss.com/us>
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


from typing import TYPE_CHECKING, Any, Dict, MutableMapping

from .shared import safe_print

if TYPE_CHECKING:
    from aqt.profiles import ProfileManager


class MetaStorageAdapter:
    """
    Adapter for Anki's meta storage object

    Used to store cross-profile information. Available at add-on load time.
    """

    _key_greeting_onboarding_v1_shown = "greeting_onboarding_v1_shown"

    def __init__(self, profile_manager: "ProfileManager", storage_key: str):
        self._profile_manager = profile_manager
        self._storage_key = storage_key
        self._fallback_meta: Dict[str, Any] = {}

    @property
    def greeting_onboarding_v1_shown(self) -> bool:
        return self._amboss_meta.get(self._key_greeting_onboarding_v1_shown, False)

    @greeting_onboarding_v1_shown.setter
    def greeting_onboarding_v1_shown(self, shown: bool):
        self._amboss_meta[self._key_greeting_onboarding_v1_shown] = shown

    @property
    def _amboss_meta(self) -> Dict[str, Any]:
        meta_dict = self._anki_meta.get(self._storage_key)
        if meta_dict is None:
            self._anki_meta[self._storage_key] = {}
        return self._anki_meta[self._storage_key]

    @property
    def _anki_meta(self) -> MutableMapping[str, Any]:
        """
        Return Anki meta storage object

        Fall back to dummy storage object if proper storage object cannot be
        accessed.
        """
        # Anki's meta storage object is not documented and is not typically accessed
        # by add-ons, so it might be more prone to future API changes than other
        # Anki objects. Therefore, let's be extra defensive:
        try:
            meta_dict = self._profile_manager.meta
            if not isinstance(meta_dict, MutableMapping):
                raise TypeError
            return meta_dict
        except (AttributeError, TypeError):
            safe_print("Unexpected error with accessing Anki meta storage")
            # Fall back to dummy storage object, therefore defaulting to
            # "first-run" state.
            return self._fallback_meta
