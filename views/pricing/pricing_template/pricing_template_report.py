#!/usr/bin/env python3

# Filename: pricing_template_report.py

"""This app is for the Amadeus automation tasks."""


from PyQt5 import QtCore, QtGui, QtWidgets


class Pricing_Template_Report(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        #Dialog.resize(1020, 900)
        Dialog.resize(800, 700)
        Dialog.setSizeGripEnabled(True)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_Bar = mpltWidgetBar(Dialog)
        self.widget_Bar.setObjectName("widget_Bar")
        self.gridLayout.addWidget(self.widget_Bar, 0, 0, 1,2)
        # self.widget_Pie = mpltWidgetPie(Dialog)
        # self.widget_Pie.setObjectName("widget_Pie")
        # self.gridLayout.addWidget(self.widget_Pie, 0, 1, 1, 1)
        self._lblTable = QtWidgets.QLabel(Dialog)
        self._lblTable.setObjectName("_lblTable")
        self._lblTable.setFont(QtGui.QFont("MS Shell Dlg 2", 10))
        self.gridLayout.addWidget(self._lblTable, 2, 0, 1, 2)
        self._tblMissingColumns = QtWidgets.QTableView(Dialog)
        self._tblMissingColumns.setAlternatingRowColors(True)
        self._tblMissingColumns.setObjectName("_tblMissingColumns")
        self._tblMissingColumns.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addWidget(self._tblMissingColumns, 3, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.label.setFont(QtGui.QFont("MS Shell Dlg 2", 10))
        self.verticalLayout.addWidget(self.label)
        self._te_templates = QtWidgets.QTextEdit(Dialog)
        self._te_templates.setObjectName("_te_templates")
        self._te_templates.setReadOnly(True)
        self.verticalLayout.addWidget(self._te_templates)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        # spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QtGui.QFont("MS Shell Dlg 2", 10))
        self.verticalLayout_2.addWidget(self.label_2)
        self._te_usagetype = QtWidgets.QTextEdit(Dialog)
        self._te_usagetype.setObjectName("_te_usagetype")
        self._te_usagetype.setReadOnly(True)
        self.verticalLayout_2.addWidget(self._te_usagetype)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 4, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self._btnClose = QtWidgets.QPushButton(Dialog)
        self._btnClose.setEnabled(True)
        self._btnClose.setMinimumSize(QtCore.QSize(60, 30))
        self._btnClose.setSizeIncrement(QtCore.QSize(60, 0))
        self._btnClose.setObjectName("_btnClose")
        self.horizontalLayout.addWidget(self._btnClose)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 2)
        self.widget_Bar.raise_()
        self._tblMissingColumns.raise_()
        # self.widget_Pie.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Pricing Template Report"))
        self.label.setText(_translate("Dialog", "Usage Type without Templates:"))
        self._lblTable.setText(_translate("Dialog", "List of columns with no mappings:"))
        self.label_2.setText(_translate("Dialog", "Missing Usage Types:"))
        self._btnClose.setText(_translate("Dialog", "Close"))

from views.pricing.pricing_template.mpltwidgetbar import mpltWidgetBar
