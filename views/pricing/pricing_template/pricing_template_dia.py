# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PricingTemplate.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
from PyQt5 import QtCore, QtGui, QtWidgets

class Pricing_Template_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(400, 400)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.font = QtGui.QFont()
        self.font.setFamily("MS Shell Dlg 2")
        self.font.setPointSize(7)
        self._icons = QtWidgets.QFileIconProvider()
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.g_layout = QtWidgets.QGridLayout()
        self.g_layout.setObjectName("g_layout")
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.g_layout.addWidget(self.line_2, 11, 0, 1, 2)
        self._leKeyword = QtWidgets.QLineEdit(Dialog)
        self._leKeyword.setObjectName("_leKeyword")
        self.g_layout.addWidget(self._leKeyword, 6, 0, 1, 1)
        self._lblOutputFolder = QtWidgets.QLabel(Dialog)
        self._lblOutputFolder.setObjectName("_lblOutputFolder")
        self.g_layout.addWidget(self._lblOutputFolder, 2, 0, 1, 1)
        self._lblUsageFlow = QtWidgets.QLabel(Dialog)
        self._lblUsageFlow.setObjectName("_lblUsageFlow")
        self.g_layout.addWidget(self._lblUsageFlow, 7, 0, 1, 1)
        self._btnGenerate = QtWidgets.QPushButton(Dialog)
        self._btnGenerate.setObjectName("_btnGenerate")
        self.g_layout.addWidget(self._btnGenerate, 12, 0, 1, 2)
        self._btnChangeSrc = QtWidgets.QPushButton(Dialog)
        self._btnChangeSrc.setObjectName("_btnChangeSrc")
        self._btnChangeSrc.setToolTip("Change Source Folder")
        self._btnChangeSrc.setIcon(self._icons.icon(self._icons.Folder))
        self._btnChangeSrc.setIconSize(QtCore.QSize(32,32))
        self._btnChangeSrc.setFlat(True)
        self.g_layout.addWidget(self._btnChangeSrc, 0, 1, 1, 1)
        self._lvUsageFlow = QtWidgets.QListWidget(Dialog)
        self._lvUsageFlow.setObjectName("_lvUsageFlow")
        self._lvUsageFlow.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.g_layout.addWidget(self._lvUsageFlow, 9, 0, 1, 2)
        self._btnChangeOut = QtWidgets.QPushButton(Dialog)
        self._btnChangeOut.setObjectName("_btnChangeOut")
        self._btnChangeOut.setToolTip("Change Output Folder")
        self._btnChangeOut.setIcon(self._icons.icon(self._icons.Folder))
        self._btnChangeOut.setIconSize(QtCore.QSize(32,32))
        self._btnChangeOut.setFlat(True)
        self.g_layout.addWidget(self._btnChangeOut, 2, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self._lblProgress = QtWidgets.QLabel(Dialog)
        self._lblProgress.setFont(self.font)
        self._lblProgress.setObjectName("_lblProgress")
        self.verticalLayout_2.addWidget(self._lblProgress, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        self._progressBar = QtWidgets.QProgressBar(Dialog)
        self._progressBar.setProperty("value", 100)
        self._progressBar.setTextVisible(False)
        self._progressBar.setObjectName("_progressBar")
        self.verticalLayout_2.addWidget(self._progressBar)
        self.g_layout.addLayout(self.verticalLayout_2, 15, 0, 2, 2)
        self._lblSourceFolder = QtWidgets.QLabel(Dialog)
        self._lblSourceFolder.setObjectName("_lblSourceFolder")
        self.g_layout.addWidget(self._lblSourceFolder, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.g_layout.addWidget(self.line, 4, 0, 1, 2)
        self._lblKeyword = QtWidgets.QLabel(Dialog)
        self._lblKeyword.setObjectName("_lblKeyword")
        self.g_layout.addWidget(self._lblKeyword, 5, 0, 1, 1)
        self._leOutputFolder = QtWidgets.QLineEdit(Dialog)
        self._leOutputFolder.setObjectName("_leOutputFolder")
        self._leOutputFolder.setFont(self.font)
        self._leOutputFolder.setReadOnly(True)
        self._leOutputFolder.setText(os.getcwd() + "\\output")
        self.g_layout.addWidget(self._leOutputFolder, 3, 0, 1, 2)
        self._cbUsageFlows = QtWidgets.QComboBox(Dialog)
        self._cbUsageFlows.setObjectName("_cbUsageFlows")
        self.g_layout.addWidget(self._cbUsageFlows, 8, 0, 1, 1)
        self._btnDelete = QtWidgets.QPushButton(Dialog)
        self._btnDelete.setObjectName("_btnDelete")
        self._btnDelete.setIcon(self._icons.icon(self._icons.Trashcan))
        self._btnDelete.setIconSize(QtCore.QSize(32,32))
        self._btnDelete.setFlat(True)
        self.g_layout.addWidget(self._btnDelete, 8, 1, 1, 1)
        self._leSourceFolder = QtWidgets.QLineEdit(Dialog)
        self._leSourceFolder.setObjectName("_leSourceFolder")
        self._leSourceFolder.setFont(self.font)
        self._leSourceFolder.setReadOnly(True)
        self._leSourceFolder.setText(os.getcwd() + "\\resources\\Pricing Templates\\Source")
        self.g_layout.addWidget(self._leSourceFolder, 1, 0, 1, 2)
        self.gridLayout.addLayout(self.g_layout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pricing Template"))
        self._lblOutputFolder.setText(_translate("Dialog", "Output Folder:"))
        self._lblUsageFlow.setText(_translate("Dialog", "Select Usage Flows:"))
        self._btnGenerate.setText(_translate("Dialog", "Generate"))
        #self._btnChangeSrc.setText(_translate("Dialog", "Change"))
        #self._btnChangeOut.setText(_translate("Dialog", "Change"))
        self._lblProgress.setText(_translate("Dialog", "ARBK - Filter Dataframe"))
        self._lblSourceFolder.setText(_translate("Dialog", "Source Folder:"))
        self._lblKeyword.setText(_translate("Dialog", "Enter Keyword:"))
        self._btnDelete.setText(_translate("Dialog", ""))

    def updateWindowTitle(self, Dialog, title):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", title))