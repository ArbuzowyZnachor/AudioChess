# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gameUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_gameMenu(object):
    def setupUi(self, gameMenu):
        gameMenu.setObjectName("gameMenu")
        gameMenu.resize(1472, 886)
        gameMenu.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(gameMenu)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_buttons = QtWidgets.QWidget(gameMenu)
        self.horizontalLayout_buttons.setStyleSheet(".QWidget{\n"
"border-image: url(:/Images/background.JPG) 0 0 0 0 stretch stretch;\n"
"background-position: center;\n"
"background-repeat: none;\n"
"}\n"
".QPushButton:hover{ \n"
"border-color: red;\n"
"}\n"
".QPushButton{\n"
"padding:15px;\n"
"background-color: white;\n"
" border-style: solid;\n"
" border-width:3px;\n"
"border-color: black;\n"
" border-radius:50px;\n"
" min-width:100px;\n"
" min-height:100px;\n"
"font-size:90pt;\n"
"}")
        self.horizontalLayout_buttons.setObjectName("horizontalLayout_buttons")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayout_buttons)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_buttons = QtWidgets.QVBoxLayout()
        self.verticalLayout_buttons.setObjectName("verticalLayout_buttons")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem1)
        self.pushButtonSingle = QtWidgets.QPushButton(self.horizontalLayout_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSingle.sizePolicy().hasHeightForWidth())
        self.pushButtonSingle.setSizePolicy(sizePolicy)
        self.pushButtonSingle.setMinimumSize(QtCore.QSize(136, 136))
        font = QtGui.QFont()
        font.setPointSize(90)
        self.pushButtonSingle.setFont(font)
        self.pushButtonSingle.setObjectName("pushButtonSingle")
        self.verticalLayout_buttons.addWidget(self.pushButtonSingle)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem2)
        self.pushButtonMulti = QtWidgets.QPushButton(self.horizontalLayout_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonMulti.sizePolicy().hasHeightForWidth())
        self.pushButtonMulti.setSizePolicy(sizePolicy)
        self.pushButtonMulti.setMinimumSize(QtCore.QSize(136, 136))
        font = QtGui.QFont()
        font.setPointSize(90)
        self.pushButtonMulti.setFont(font)
        self.pushButtonMulti.setObjectName("pushButtonMulti")
        self.verticalLayout_buttons.addWidget(self.pushButtonMulti)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem3)
        self.pushButtonExit = QtWidgets.QPushButton(self.horizontalLayout_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonExit.sizePolicy().hasHeightForWidth())
        self.pushButtonExit.setSizePolicy(sizePolicy)
        self.pushButtonExit.setMinimumSize(QtCore.QSize(136, 136))
        font = QtGui.QFont()
        font.setPointSize(90)
        self.pushButtonExit.setFont(font)
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.verticalLayout_buttons.addWidget(self.pushButtonExit)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_buttons.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout_buttons)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.gridLayout.addWidget(self.horizontalLayout_buttons, 0, 0, 1, 1)

        self.retranslateUi(gameMenu)
        QtCore.QMetaObject.connectSlotsByName(gameMenu)

    def retranslateUi(self, gameMenu):
        _translate = QtCore.QCoreApplication.translate
        gameMenu.setWindowTitle(_translate("gameMenu", "Form"))
        self.pushButtonSingle.setText(_translate("gameMenu", "vs Komputer"))
        self.pushButtonMulti.setText(_translate("gameMenu", "Online"))
        self.pushButtonExit.setText(_translate("gameMenu", "Powrót"))
from . import Images_rc
