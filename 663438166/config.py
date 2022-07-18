# Copyright (c) ijgnord.

import os
from aqt import mw


def gc(arg, fail=False):
    conf = mw.addonManager.getConfig(__name__)
    if conf:
        return conf.get(arg, fail)
    else:
        return fail

addon_folder_abs_path = os.path.dirname(__file__)
foldername = os.path.basename(addon_folder_abs_path)  # mw.addonManager.addonFromModule(__name__)
addonname = mw.addonManager.addonName(foldername)
user_files_folder = os.path.join(addon_folder_abs_path, "user_files")
addons_pickle = os.path.join(user_files_folder, "new_cards_day_verify.pickle")
