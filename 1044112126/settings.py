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


from enum import Enum
from typing import Dict, List, Union

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtGui import QColor, QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (
    QCheckBox,
    QColorDialog,
    QDialog,
    QDialogButtonBox,
    QKeySequenceEdit,
    QPushButton,
    QWidget,
)

from .config import (
    AddonConfig,
    ColorSettingName,
    DisplaySettingName,
    HotkeySettingName,
)

# TODO: find a way to not ignore Qt forms when type checking
from .gui.forms.anki21.settings import Ui_Settings  # type: ignore
from .hooks import amboss_did_login, amboss_did_logout
from .shared import _


class WidgetClass(Enum):
    KEYSEQUENCE = "QKeySequenceEdit"
    CHECKBOX = "QCheckBox"
    COLORPICKER = "QColorButton"


class QColorButton(QPushButton):
    def __init__(self, parent: QWidget = None, color: str = "#000000"):
        super().__init__(parent=parent)
        self._set_button_color(color)
        self.clicked.connect(self._choose_color)

    def color(self) -> str:
        """Get current color

        :return: HTML color code
        """
        return self._color

    def set_color(self, color: str):
        """Set current color

        :param color: HTML color code
        """
        self._set_button_color(color)

    @pyqtSlot()
    def _choose_color(self) -> None:
        dialog = QColorDialog(parent=self)
        color = dialog.getColor(QColor(self._color))
        if not color.isValid():
            return
        self._set_button_color(color.name())

    def _set_button_color(self, color: str):
        """Set preview color"""
        pixmap = QPixmap(128, 18)
        qcolor = QColor(0, 0, 0)
        qcolor.setNamedColor(color)
        pixmap.fill(qcolor)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(QSize(128, 18))
        self._color = color


class SettingsDialog(QDialog):

    _widgets: Dict[WidgetClass, List[str]] = {
        WidgetClass.KEYSEQUENCE: [setting.value for setting in HotkeySettingName],
        WidgetClass.CHECKBOX: [setting.value for setting in DisplaySettingName],
        WidgetClass.COLORPICKER: [setting.value for setting in ColorSettingName],
    }

    def __init__(self, addon_config: AddonConfig, parent: QWidget):
        super().__init__(parent=parent)
        self._addon_config = addon_config
        self._form = Ui_Settings()
        self._form.setupUi(self)
        self.setObjectName("amboss_settings_dialog")
        self._translate_ui()
        self._setup_custom_widgets()
        self._form.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(
            self.on_restore_defaults
        )
        amboss_did_login.append(self._on_login_hook)
        amboss_did_logout.append(self._on_logout_hook)

    def show_modal(self):
        self.load_config(self._addon_config)
        self._form.enablePopupDefinitions.setFocus()
        self.exec_()

    def load_config(self, config: Union[dict, AddonConfig]):
        # TODO: revisit setting and getting widget state once we refactor the
        # config system
        for widget_name in self._widgets[WidgetClass.KEYSEQUENCE]:
            key_widget: QKeySequenceEdit = getattr(self._form, widget_name)
            key_widget.setKeySequence(QKeySequence(config[widget_name]))

        for widget_name in self._widgets[WidgetClass.CHECKBOX]:
            checkbox: QCheckBox = getattr(self._form, widget_name)
            checkbox.setChecked(config[widget_name])

        for widget_name in self._widgets[WidgetClass.COLORPICKER]:
            color_picker: QColorButton = getattr(self._form, widget_name)
            color_picker.set_color(config[widget_name])

    def save_config(self):
        config = self._addon_config

        for widget_name in self._widgets[WidgetClass.KEYSEQUENCE]:
            key_widget: QKeySequenceEdit = getattr(self._form, widget_name)
            config[widget_name] = key_widget.keySequence().toString()

        for widget_name in self._widgets[WidgetClass.CHECKBOX]:
            checkbox: QCheckBox = getattr(self._form, widget_name)
            config[widget_name] = checkbox.isChecked()

        for widget_name in self._widgets[WidgetClass.COLORPICKER]:
            color_picker: QColorButton = getattr(self._form, widget_name)
            config[widget_name] = color_picker.color()

        self._addon_config.save()

    def on_restore_defaults(self):
        self.load_config(self._addon_config.defaults())

    def accept(self):
        self.save_config()
        super().accept()

    def _setup_custom_widgets(self):
        highlight_color_button = QColorButton(self)
        self._form.layoutColorButton.addWidget(highlight_color_button)

        self._form.styleColorHighlights = (  # type: ignore[attr-defined]
            highlight_color_button
        )

    def _on_login_hook(self):
        self.load_config(self._addon_config)

        highlight_color_button: QColorButton = (
            self._form.styleColorHighlights  # type: ignore[attr-defined]
        )
        highlight_color_button.setDisabled(False)

        for widget_name in self._widgets[WidgetClass.KEYSEQUENCE]:
            key_widget: QKeySequenceEdit = getattr(self._form, widget_name)
            key_widget.setDisabled(False)

        enable_article_viewer_checkbox: QCheckBox = getattr(
            self._form, DisplaySettingName.ENABLE_ARTICLE_VIEWER.value
        )
        enable_article_viewer_checkbox.setDisabled(False)

        self.save_config()

    def _on_logout_hook(self):
        self.load_config(self._addon_config)

        highlight_color_button: QColorButton = (
            self._form.styleColorHighlights  # type: ignore[attr-defined]
        )
        highlight_color_button.setDisabled(False)

        for widget_name in self._widgets[WidgetClass.KEYSEQUENCE]:
            key_widget: QKeySequenceEdit = getattr(self._form, widget_name)
            key_widget.setDisabled(True)

        enable_article_viewer_checkbox: QCheckBox = getattr(
            self._form, DisplaySettingName.ENABLE_ARTICLE_VIEWER.value
        )
        enable_article_viewer_checkbox.setChecked(True)
        enable_article_viewer_checkbox.setDisabled(True)

        self.save_config()

    def _translate_ui(self):
        self.setWindowTitle(_("AMBOSS - Settings"))
        self._form.label_8.setText(_("AMBOSS Add-on Settings"))
        self._form.label.setText(_("General"))
        self._form.enablePopupDefinitions.setToolTip(
            _(
                "Underline important phrases on your cards and provide hover definitions for them"
            )
        )
        self._form.enablePopupDefinitions.setText(_("&Enable pop-up definitions"))
        self._form.enablePopupDefinitonsOnQuestions.setToolTip(
            _(
                "Toggle between showing definitions on both card sides or on the answer side only"
            )
        )
        self._form.enablePopupDefinitonsOnQuestions.setText(
            _("Show pop-up definitions on &questions")
        )
        self._form.label_4.setText(_("Styling"))
        self._form.label_6.setText(_("Highlight color"))
        self._form.label_2.setText(_("Keyboard Shortcuts"))
        self._form.label_3.setText(_("Open next pop-up"))
        self._form.label_5.setText(_("Open previous pop-up"))
        self._form.label_7.setText(_("Close pop-up"))
        self._form.enableArticleViewer.setToolTip(
            _("Whether to open AMBOSS articles within Anki or an external web browser")
        )
        self._form.enableArticleViewer.setText(_("Open &articles in Anki (beta)"))
        self._form.label_9.setText(_("Toggle side panel"))
        self._form.buttonBox.button(QDialogButtonBox.RestoreDefaults).setText(
            _("Restore Defaults")
        )
        self._form.buttonBox.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        self._form.buttonBox.button(QDialogButtonBox.Save).setText(_("Save"))
