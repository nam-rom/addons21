# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'build/dist/designer/sidepanel.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SidePanel(object):
    def setupUi(self, SidePanel):
        SidePanel.setObjectName("SidePanel")
        SidePanel.resize(400, 500)
        SidePanel.setMinimumSize(QtCore.QSize(624, 0))
        self.mainLayout = QtWidgets.QVBoxLayout(SidePanel)
        self.mainLayout.setContentsMargins(0, 6, 0, 0)
        self.mainLayout.setObjectName("mainLayout")
        self.layout_navbar = QtWidgets.QVBoxLayout()
        self.layout_navbar.setSpacing(0)
        self.layout_navbar.setObjectName("layout_navbar")
        self.mainLayout.addLayout(self.layout_navbar)
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_main.setObjectName("layout_main")
        self.mainLayout.addLayout(self.layout_main)
        self.mainLayout.setStretch(1, 10)

        self.retranslateUi(SidePanel)
        QtCore.QMetaObject.connectSlotsByName(SidePanel)

    def retranslateUi(self, SidePanel):
        _translate = QtCore.QCoreApplication.translate
        SidePanel.setWindowTitle(_translate("SidePanel", "SidePanel"))
