#!/usr/bin/env python3

# Filename: template_warning_dia.py

"""This app is for the Amadeus automation tasks."""

from PyQt5 import QtCore, QtGui, QtWidgets


class Template_Warning_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(277, 155)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self._lblWarning = QtWidgets.QLabel(Dialog)
        self._lblWarning.setObjectName("_lblWarning")
        self.verticalLayout_2.addWidget(self._lblWarning)
        self._lblContinue = QtWidgets.QLabel(Dialog)
        self._lblContinue.setObjectName("_lblContinue")
        self.verticalLayout_2.addWidget(self._lblContinue)
        self._teUsageTypes = QtWidgets.QTextEdit(Dialog)
        self._teUsageTypes.setEnabled(True)
        self._teUsageTypes.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._teUsageTypes.setFrameShadow(QtWidgets.QFrame.Raised)
        self._teUsageTypes.setLineWidth(1)
        self._teUsageTypes.setReadOnly(True)
        self._teUsageTypes.setObjectName("_teUsageTypes")
        self.verticalLayout_2.addWidget(self._teUsageTypes)
        self._btnBox = QtWidgets.QDialogButtonBox(Dialog)
        self._btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._btnBox.setObjectName("_btnBox")
        self.verticalLayout_2.addWidget(self._btnBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Warning: No Template found"))
        self._lblWarning.setText(_translate("Dialog", "Warning: No templates found for the usage type below."))
        self._lblContinue.setText(_translate("Dialog", "Do you still wish to continue?"))
        # self._teUsageTypes.setHtml(_translate("Dialog", ""))