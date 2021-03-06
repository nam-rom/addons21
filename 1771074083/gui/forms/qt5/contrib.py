# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'build/dist/designer/contrib.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.contribLayout = QtWidgets.QVBoxLayout()
        self.contribLayout.setContentsMargins(-1, 5, -1, 10)
        self.contribLayout.setObjectName("contribLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.labHeart = QtWidgets.QLabel(Dialog)
        self.labHeart.setText("")
        self.labHeart.setPixmap(QtGui.QPixmap("review_heatmap:icons/heart.svg"))
        self.labHeart.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labHeart.setObjectName("labHeart")
        self.horizontalLayout_3.addWidget(self.labHeart)
        self.fmtLabContrib = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.fmtLabContrib.setFont(font)
        self.fmtLabContrib.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.fmtLabContrib.setObjectName("fmtLabContrib")
        self.horizontalLayout_3.addWidget(self.fmtLabContrib)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.contribLayout.addLayout(self.horizontalLayout_3)
        self.fmtLabHeader = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fmtLabHeader.sizePolicy().hasHeightForWidth())
        self.fmtLabHeader.setSizePolicy(sizePolicy)
        self.fmtLabHeader.setWordWrap(True)
        self.fmtLabHeader.setOpenExternalLinks(False)
        self.fmtLabHeader.setObjectName("fmtLabHeader")
        self.contribLayout.addWidget(self.fmtLabHeader)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.contribLayout.addItem(spacerItem2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btnPatreon = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPatreon.sizePolicy().hasHeightForWidth())
        self.btnPatreon.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("review_heatmap:icons/patreon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPatreon.setIcon(icon)
        self.btnPatreon.setIconSize(QtCore.QSize(32, 32))
        self.btnPatreon.setObjectName("btnPatreon")
        self.gridLayout.addWidget(self.btnPatreon, 1, 0, 1, 2)
        self.contribLayout.addLayout(self.gridLayout)
        self.labFooter = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labFooter.sizePolicy().hasHeightForWidth())
        self.labFooter.setSizePolicy(sizePolicy)
        self.labFooter.setWordWrap(True)
        self.labFooter.setObjectName("labFooter")
        self.contribLayout.addWidget(self.labFooter)
        self.verticalLayout.addLayout(self.contribLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnCredits = QtWidgets.QPushButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("review_heatmap:icons/heart.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnCredits.setIcon(icon1)
        self.btnCredits.setObjectName("btnCredits")
        self.horizontalLayout_2.addWidget(self.btnCredits)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.btnPatreon, self.btnCredits)
        Dialog.setTabOrder(self.btnCredits, self.buttonBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Please support my work"))
        self.fmtLabContrib.setText(_translate("Dialog", "Love {ADDON_NAME}?"))
        self.fmtLabHeader.setText(_translate("Dialog", "<html><head/><body><p>Hi! <strong>Glutanimate</strong> here :) Thanks for checking out Review Heatmap and some of my other add-ons. I hope you\'ve been enjoying them! </p><p>If <strong>{ADDON_NAME}</strong> or any of <a href=\"action://installed-addons\"><span style=\" text-decoration: underline; color:#2980b9;\">my other projects</span></a> has been a valuable asset in your studies, please do consider <strong>supporting my work</strong>:</p></body></html>"))
        self.btnPatreon.setToolTip(_translate("Dialog", "Perks include access to Patron-only add-ons, <br>exclusive blog posts, mentions in the credits, and more!"))
        self.btnPatreon.setText(_translate("Dialog", "Become a Patron and receive \n"
"exclusive add-ons && other goodies!"))
        self.labFooter.setText(_translate("Dialog", "<html><head/><body><p>Each contribution is greatly appreciated and will help me <strong>update and improve</strong> my add-ons as time goes by! Thank you.</p></body></html>"))
        self.btnCredits.setText(_translate("Dialog", "Credits"))
