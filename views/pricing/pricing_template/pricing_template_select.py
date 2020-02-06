#!/usr/bin/env python3

# Filename: pricing_template_select.py

"""This app is for the Amadeus automation tasks."""

from PyQt5 import QtCore, QtGui, QtWidgets


class Pricing_Template_Select(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(154, 107)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rbtnDebit = QtWidgets.QRadioButton(self.groupBox)
        self.rbtnDebit.setChecked(True)
        self.rbtnDebit.setObjectName("rbtnDebit")
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.rbtnDebit)
        self.verticalLayout.addWidget(self.rbtnDebit)
        self.rbtnCredit = QtWidgets.QRadioButton(self.groupBox)
        self.rbtnCredit.setObjectName("rbtnCredit")
        self.buttonGroup.addButton(self.rbtnCredit)
        self.verticalLayout.addWidget(self.rbtnCredit)
        self.rbtnAll = QtWidgets.QRadioButton(self.groupBox)
        self.rbtnAll.setChecked(False)
        self.rbtnAll.setObjectName("rbtnAll")
        self.buttonGroup.addButton(self.rbtnAll)
        self.verticalLayout.addWidget(self.rbtnAll)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Selection"))
        self.groupBox.setTitle(_translate("Dialog", "Select Pricing Template To Process"))
        self.rbtnDebit.setText(_translate("Dialog", "Debit - MA"))
        self.rbtnCredit.setText(_translate("Dialog", "Credit - PA"))
        self.rbtnAll.setText(_translate("Dialog", "All"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
