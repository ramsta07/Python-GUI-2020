#!/usr/bin/env python3

# Filename: pricing_template_finish.py

"""This app is for the Amadeus automation tasks."""

from PyQt5 import QtCore, QtGui, QtWidgets


class PricingTemplate_finish(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(700, 132)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.lblTotal = QtWidgets.QLabel(Dialog)
        self.lblTotal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lblTotal.setObjectName("lblTotal")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lblTotal)
        self._leTotalTemp = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._leTotalTemp.sizePolicy().hasHeightForWidth())
        self._leTotalTemp.setSizePolicy(sizePolicy)
        self._leTotalTemp.setReadOnly(True)
        self._leTotalTemp.setObjectName("_leTotalTemp")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._leTotalTemp)
        self.lblOutput = QtWidgets.QLabel(Dialog)
        self.lblOutput.setObjectName("lblOutput")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblOutput)
        self.lblElapTime = QtWidgets.QLabel(Dialog)
        self.lblElapTime.setObjectName("lblElapTime")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lblElapTime)
        self._le_TotalTime = QtWidgets.QLineEdit(Dialog)
        self._le_TotalTime.setReadOnly(True)
        self._le_TotalTime.setObjectName("_le_TotalTime")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self._le_TotalTime)
        self._teOutputFolder = QtWidgets.QTextEdit(Dialog)
        self._teOutputFolder.setReadOnly(True)
        self._teOutputFolder.setObjectName("_teOutputFolder")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self._teOutputFolder)
        self.gridLayout.addLayout(self.formLayout_2, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self._btnReport = QtWidgets.QPushButton(Dialog)
        self._btnReport.setObjectName("_btnReport")
        self.horizontalLayout.addWidget(self._btnReport)
        self._btnClose = QtWidgets.QPushButton(Dialog)
        self._btnClose.setObjectName("_btnClose")
        self.horizontalLayout.addWidget(self._btnClose)
        spacerItem1 = QtWidgets.QSpacerItem(32, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pricing Template - Finished"))
        self.lblTotal.setText(_translate("Dialog", "Total Pricing Template Processed:"))
        self.lblOutput.setText(_translate("Dialog", "  Pricing Template Output Folder:"))
        self.lblElapTime.setText(_translate("Dialog", "                    Total Elapsed Time:"))
        self._teOutputFolder.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">C:\\Users\\rampil.saavedra\\OneDrive - Accenture\\Assignment\\Amadeus DS App\\output</p></body></html>"))
        self._btnReport.setText(_translate("Dialog", "View Report"))
        self._btnClose.setText(_translate("Dialog", "Close"))