# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pricing_template_report.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(408, 433)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self._tblMissingColumns = QtWidgets.QTableWidget(Form)
        self._tblMissingColumns.setMinimumSize(QtCore.QSize(0, 200))
        self._tblMissingColumns.setAlternatingRowColors(True)
        self._tblMissingColumns.setObjectName("_tblMissingColumns")
        self._tblMissingColumns.setColumnCount(0)
        self._tblMissingColumns.setRowCount(0)
        self.gridLayout.addWidget(self._tblMissingColumns, 1, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.textEdit_2 = QtWidgets.QTextEdit(Form)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout_2.addWidget(self.textEdit_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self._btnClose = QtWidgets.QPushButton(Form)
        self._btnClose.setEnabled(True)
        self._btnClose.setMinimumSize(QtCore.QSize(60, 25))
        self._btnClose.setSizeIncrement(QtCore.QSize(60, 0))
        self._btnClose.setObjectName("_btnClose")
        self.horizontalLayout.addWidget(self._btnClose)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)
        self.widget_Bar = mpltWidgetBar(Form)
        self.widget_Bar.setObjectName("widget_Bar")
        self.gridLayout.addWidget(self.widget_Bar, 0, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Usage Type without Templates:"))
        self.label_2.setText(_translate("Form", "Missing Usage Types:"))
        self._btnClose.setText(_translate("Form", "Close"))
from mpltwidgetbar import mpltWidgetBar


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
