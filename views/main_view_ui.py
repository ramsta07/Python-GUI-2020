#!/usr/bin/env python3

# Filename: main_view_ui.py

"""This app is for the Amadeus automation tasks."""

import os, sys

#Import QApplication and the required widgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

__version__ = "1.0"
__author__ = 'Ram Saavedra'

class MainView_UI(object):

	"""DSAppUi View(GUI)."""

	#======= SETUP UI =================================

	def setupUi(self, MainWindow):

		_app_path = os.getcwd() + "\\resources"
		images_path = os.path.join(_app_path, 'images')
		full_path = os.path.join(images_path, 'analytics.png')
		self._app_icon = QtGui.QIcon(full_path)

		#Set some main window's properties
		MainWindow.setWindowIcon(self._app_icon)
		flag = QtCore.Qt.WindowCloseButtonHint
		MainWindow.setWindowFlags(QtCore.Qt.Window | flag)
		MainWindow.resize(500,400)

		# Set the central widget
		self.generalLayout = QtWidgets.QVBoxLayout()
		self._centralWidget = QWidget(MainWindow)
		MainWindow.setCentralWidget(self._centralWidget)
		self._centralWidget.setLayout(self.generalLayout)

		# Create the window display and the buttons
		self._createMenuBar(MainWindow)
		self._createStatusBar(MainWindow)
		self._createHeader()
		self._createPricingOptionsBox()
		self._createContractsOptionsBox()
		self._createContractTempOptionsBox()
		self._createContractValOptionsBox()
		self._createButtons()

		self._setup_tray_icon(MainWindow)

		self.retranslateUi(MainWindow)

		self.pricing_frame.hide()
		self.contracts_frame.hide()
		self.contracts_temp_frame.hide()
		self.contracts_val_frame.hide()

	def _createHeader(self):
		"""Create the Title"""

		self.title = QtWidgets.QLabel()

		# Set some display's properties
		font = QtGui.QFont()
		font.setFamily("Calibri")
		font.setPointSize(36)

		self.title.setFont(font)

		self.headerLayout = QtWidgets.QVBoxLayout()

		# Add the display to the general layout

		self.headerLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter)
		self.generalLayout.addLayout(self.headerLayout)

	def _createPricingOptionsBox(self):

		# create the frame object.
		self.pricing_frame = QtWidgets.QFrame()

		self.pricing_hlayout = QtWidgets.QHBoxLayout()
		pricing_gb = QtWidgets.QGroupBox('Choose Pricing Options')
		self.pricing_layout = QtWidgets.QHBoxLayout(pricing_gb)

		self.btnPricingTemp = QtWidgets.QPushButton()
		self.btnPricingVal = QtWidgets.QPushButton()

		self.pricing_layout.addWidget(self.btnPricingTemp)
		self.pricing_layout.addWidget(self.btnPricingVal)

		self.pricing_hlayout.addWidget(pricing_gb)

		self.pricing_frame.setLayout(self.pricing_hlayout)

		self.generalLayout.addWidget(self.pricing_frame)

	def _createContractsOptionsBox(self):

		# create the frame object.
		self.contracts_frame = QtWidgets.QFrame()

		self.contracts_hlayout = QtWidgets.QHBoxLayout()
		contracts_gb = QtWidgets.QGroupBox('Choose Contracts Options')
		self.contracts_layout = QtWidgets.QHBoxLayout(contracts_gb)

		self.btnContTypeOpt = QtWidgets.QPushButton()
		self.contracts_layout.addWidget(self.btnContTypeOpt)

		self.btnContValOpt = QtWidgets.QPushButton()
		self.contracts_layout.addWidget(self.btnContValOpt)

		self.contracts_hlayout.addWidget(contracts_gb)

		self.contracts_frame.setLayout(self.contracts_hlayout)

		self.generalLayout.addWidget(self.contracts_frame)

	def _createContractTempOptionsBox(self):

		# create the frame object.
		self.contracts_temp_frame = QtWidgets.QFrame()

		self.contracts_hlayout = QtWidgets.QHBoxLayout()
		contracts_gb = QtWidgets.QGroupBox('Choose Contract Template')
		self.contracts_layout = QtWidgets.QVBoxLayout(contracts_gb)

		self.btnContTypeTemp = QtWidgets.QPushButton()
		self.contracts_layout.addWidget(self.btnContTypeTemp)

		self.btnDebCdtTemp = QtWidgets.QPushButton()
		self.contracts_layout.addWidget(self.btnDebCdtTemp)

		self.contracts_hlayout.addWidget(contracts_gb)

		self.contracts_temp_frame.setLayout(self.contracts_hlayout)

		self.generalLayout.addWidget(self.contracts_temp_frame)

	def _createContractValOptionsBox(self):

		# create the frame object.
		self.contracts_val_frame = QtWidgets.QFrame()

		self.contracts_hlayout = QtWidgets.QHBoxLayout()
		contracts_gb = QtWidgets.QGroupBox('Choose Contract Validation')
		self.contracts_layout = QtWidgets.QHBoxLayout(contracts_gb)

		self.btnContStep1 = QtWidgets.QPushButton()
		self.contracts_layout.addWidget(self.btnContStep1)

		self.btnContStep3 = QtWidgets.QPushButton()
		self.contracts_layout.addWidget(self.btnContStep3)

		self.contracts_hlayout.addWidget(contracts_gb)

		self.contracts_val_frame.setLayout(self.contracts_hlayout)

		self.generalLayout.addWidget(self.contracts_val_frame)


	def _createButtons(self):
		"""Create the buttons"""

		self.buttonLayout = QtWidgets.QHBoxLayout()
		#self.buttonLayout.addStretch(1)

		self.btnPricing = QtWidgets.QPushButton()
		self.buttonLayout.addWidget(self.btnPricing)

		self.btnContracts = QtWidgets.QPushButton()
		self.buttonLayout.addWidget(self.btnContracts)

		# Add the display to the general layout
		self.generalLayout.addLayout(self.buttonLayout)

	def _createMenuBar(self, MainWindow):
		"""Create the Menu Bar"""

		self.menubar = QtWidgets.QMenuBar()
		self.menubar.setGeometry(QtCore.QRect(0, 0, 302, 18))
		self.menuFile = QtWidgets.QMenu(self.menubar)
		self.menuHelp = QtWidgets.QMenu(self.menubar)

		self.actionExit = QtWidgets.QAction()
		self.actionAbout = QtWidgets.QAction()
		self.menuFile.addAction(self.actionExit)
		self.menuHelp.addAction(self.actionAbout)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuHelp.menuAction())

		MainWindow.setMenuBar(self.menubar)

	def _createStatusBar(self, MainWindow):

		"""Create the status bar"""

		self.statusbar = QtWidgets.QStatusBar()
		MainWindow.setStatusBar(self.statusbar)
	
	def _setup_tray_icon(self, MainWindow):
		tray_icon = QtWidgets.QSystemTrayIcon(MainWindow)
		tray_icon.setIcon(self._app_icon)
		tray_icon.setToolTip('DS Amadeus App')

		tray_menu = QtWidgets.QMenu(MainWindow)
		tray_menu.addAction('Open', MainWindow.show)
		q = QtWidgets.QAction('Quit', MainWindow, triggered=MainWindow._close)
		tray_menu.addAction(q)
		tray_icon.setContextMenu(tray_menu)
		tray_icon.show()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "DS Amadeus App v1.0"))
		self.title.setText(_translate("MainWindow", "AMADEUS"))
		self.btnPricing.setText(_translate("MainWindow", "Pricing"))
		self.btnContracts.setText(_translate("MainWindow", "Contracts"))
		self.btnPricingTemp.setText(_translate("MainWindow", "Pricing Template"))
		self.btnPricingVal.setText(_translate("MainWindow", "Pricing Validation"))
		self.btnContTypeOpt.setText(_translate("MainWindow", "Contract Templates"))
		self.btnContValOpt.setText(_translate("MainWindow", "Contract Validation"))
		self.btnContTypeTemp.setText(_translate("MainWindow", "Contract Type Template"))
		self.btnDebCdtTemp.setText(_translate("MainWindow", "Debit/Credit Template"))
		self.btnContStep1.setText(_translate("MainWindow", "Contract Step 1 Validation"))
		self.btnContStep3.setText(_translate("MainWindow", "Contract Step 3 Validation"))
		self.menuFile.setTitle(_translate("MainWindow", "File"))
		self.menuHelp.setTitle(_translate("MainWindow", "Help"))
		self.actionExit.setText(_translate("MainWindow", "Exit"))
		self.actionAbout.setText(_translate("MainWindow", "About"))