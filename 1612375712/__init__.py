from aqt import mw
from aqt.qt import *

def toggle_full_screen():
    mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)

action = QAction("Toggle Full Screen", mw)
action.setShortcut("F11")
action.triggered.connect(toggle_full_screen)
mw.form.menuTools.addAction(action)
