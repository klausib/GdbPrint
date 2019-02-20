# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grpEig_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmEig(object):
    def setupUi(self, frmEig):
        frmEig.setObjectName("frmEig")
        frmEig.resize(676, 285)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmEig.sizePolicy().hasHeightForWidth())
        frmEig.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(frmEig)
        self.gridLayout.setObjectName("gridLayout")
        self.tblEig = QtWidgets.QTableWidget(frmEig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblEig.sizePolicy().hasHeightForWidth())
        self.tblEig.setSizePolicy(sizePolicy)
        self.tblEig.setRowCount(0)
        self.tblEig.setColumnCount(3)
        self.tblEig.setObjectName("tblEig")
        self.tblEig.horizontalHeader().setVisible(True)
        self.tblEig.horizontalHeader().setCascadingSectionResizes(False)
        self.tblEig.horizontalHeader().setStretchLastSection(False)
        self.tblEig.verticalHeader().setVisible(True)
        self.tblEig.verticalHeader().setDefaultSectionSize(30)
        self.gridLayout.addWidget(self.tblEig, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnSel = QtWidgets.QPushButton(frmEig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSel.sizePolicy().hasHeightForWidth())
        self.btnSel.setSizePolicy(sizePolicy)
        self.btnSel.setMinimumSize(QtCore.QSize(75, 110))
        self.btnSel.setCheckable(False)
        self.btnSel.setChecked(False)
        self.btnSel.setObjectName("btnSel")
        self.verticalLayout.addWidget(self.btnSel)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btnOK = QtWidgets.QPushButton(frmEig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOK.sizePolicy().hasHeightForWidth())
        self.btnOK.setSizePolicy(sizePolicy)
        self.btnOK.setMinimumSize(QtCore.QSize(75, 110))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.btnOK.setFont(font)
        self.btnOK.setObjectName("btnOK")
        self.verticalLayout.addWidget(self.btnOK)
        spacerItem1 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(frmEig)
        QtCore.QMetaObject.connectSlotsByName(frmEig)

    def retranslateUi(self, frmEig):
        _translate = QtCore.QCoreApplication.translate
        frmEig.setWindowTitle(_translate("frmEig", "GDB-Print"))
        self.tblEig.setSortingEnabled(True)
        self.btnSel.setText(_translate("frmEig", "Alles \n"
" auswählen\n"
"/\n"
"Auswahl\n"
"löschen"))
        self.btnOK.setText(_translate("frmEig", "Karte\n"
"beschriften"))

