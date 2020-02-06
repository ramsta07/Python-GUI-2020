#!/usr/bin/env python3

# Filename: main_view_ui.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os

from PyQt5.QtWidgets import QDialog, QFileDialog, QMainWindow, QApplication, QListWidgetItem
from PyQt5 import QtCore, QtGui

#Views
from views.main_view_ui import MainView_UI

#Model
from model.ui_model import main_app_Model

#Controller
from controller.pricing_template_controller import Pricing_Template_Controller
from controller.contract_template_controller import Contract_Template_Controller

__version__ = "1.0"
__author__ = 'Ram Saavedra'

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self._app_model = main_app_Model()
        self._pt_ctrl = Pricing_Template_Controller(self, self._app_model)
        self._ct_ctrl = Contract_Template_Controller(self, self._app_model)

        self._ui = MainView_UI()
        self._ui.setupUi(self)

        # Setup Connections

        self._setupConnections()

    def _showPricingOptions(self):
        self._ui.contracts_frame.hide()
        self._ui.contracts_temp_frame.hide()
        self._ui.contracts_val_frame.hide()
        self._ui.pricing_frame.show()

    def _showContractsOptions(self):
        self._ui.pricing_frame.hide()
        self._ui.contracts_temp_frame.hide()
        self._ui.contracts_val_frame.hide()
        self._ui.contracts_frame.show()

    def _showContractTypeOptions(self):
        self._ui.contracts_frame.hide()
        self._ui.contracts_val_frame.hide()
        self._ui.contracts_temp_frame.show()

    def _showContractValOptions(self):
        self._ui.contracts_frame.hide()
        self._ui.contracts_val_frame.show()

    def _setupConnections(self):

        #======== Main UI ========#

        self._ui.btnPricing.clicked.connect(self._showPricingOptions)
        self._ui.btnContracts.clicked.connect(self._showContractsOptions)

        self._ui.btnContTypeOpt.clicked.connect(self._showContractTypeOptions)
        self._ui.btnContValOpt.clicked.connect(self._showContractValOptions)

        #========Pricing Main =========#

        self._ui.btnPricingTemp.clicked.connect(self._pt_ctrl._showPricingTemplate)
        self._ui.btnPricingVal.clicked.connect(self._pt_ctrl._showPricingValidation)

        #========Contract Main =========#

        self._ui.btnContTypeTemp.clicked.connect(self._ct_ctrl._showContractTypeTemplate)
        self._ui.btnDebCdtTemp.clicked.connect(self._ct_ctrl._showDebitCreditTemplate)

        self._ui.btnContStep1.clicked.connect(self._ct_ctrl._showContractPreValStep1Template)
        self._ui.btnContStep3.clicked.connect(self._ct_ctrl._showContractPreValStep3Template)

        #=======Menu Action========#

        self._ui.actionExit.triggered.connect(self._close)

    #==================================== COMMON =================================#

    def closeEvent(self, e):
        self.hide()
        e.ignore()

    def _close(self):
        QApplication.instance().quit()