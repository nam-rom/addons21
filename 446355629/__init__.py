# -*- coding: utf-8 -*-
from aqt.theme import theme_manager
from .darkdetect import *

theme_manager.set_night_mode(darkdetect.isDark())