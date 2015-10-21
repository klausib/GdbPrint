# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grpEig_ui.ui'
#
# Created: Mon Oct 12 09:28:54 2015
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmEig(object):
    def setupUi(self, frmEig):
        frmEig.setObjectName(_fromUtf8("frmEig"))
        frmEig.resize(676, 285)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmEig.sizePolicy().hasHeightForWidth())
        frmEig.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(frmEig)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblEig = QtGui.QTableWidget(frmEig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblEig.sizePolicy().hasHeightForWidth())
        self.tblEig.setSizePolicy(sizePolicy)
        self.tblEig.setRowCount(0)
        self.tblEig.setColumnCount(3)
        self.tblEig.setObjectName(_fromUtf8("tblEig"))
        self.tblEig.setColumnCount(3)
        self.tblEig.setRowCount(0)
        self.tblEig.horizontalHeader().setVisible(True)
        self.tblEig.horizontalHeader().setCascadingSectionResizes(False)
        self.tblEig.horizontalHeader().setStretchLastSection(False)
        self.tblEig.verticalHeader().setVisible(True)
        self.tblEig.verticalHeader().setDefaultSectionSize(30)
        self.gridLayout.addWidget(self.tblEig, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btnSel = QtGui.QPushButton(frmEig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSel.sizePolicy().hasHeightForWidth())
        self.btnSel.setSizePolicy(sizePolicy)
        self.btnSel.setMinimumSize(QtCore.QSize(75, 110))
        self.btnSel.setCheckable(False)
        self.btnSel.setChecked(False)
        self.btnSel.setObjectName(_fromUtf8("btnSel"))
        self.verticalLayout.addWidget(self.btnSel)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btnOK = QtGui.QPushButton(frmEig)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOK.sizePolicy().hasHeightForWidth())
        self.btnOK.setSizePolicy(sizePolicy)
        self.btnOK.setMinimumSize(QtCore.QSize(75, 110))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        font.setUnderline(False)
        font.setBold(True)
        self.btnOK.setFont(font)
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.verticalLayout.addWidget(self.btnOK)
        spacerItem1 = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(frmEig)
        QtCore.QMetaObject.connectSlotsByName(frmEig)

    def retranslateUi(self, frmEig):
        frmEig.setWindowTitle(QtGui.QApplication.translate("frmEig", "GDB-Print", None, QtGui.QApplication.UnicodeUTF8))
        self.tblEig.setSortingEnabled(True)
        self.btnSel.setText(QtGui.QApplication.translate("frmEig", "Alles \n"
" auswählen\n"
"/\n"
"Auswahl\n"
"löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("frmEig", "Karte\n"
"beschriften", None, QtGui.QApplication.UnicodeUTF8))

