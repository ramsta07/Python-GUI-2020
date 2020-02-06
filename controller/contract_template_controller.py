#!/usr/bin/env python3

# Filename: contract_template_controller.py

"""This app is for the Amadeus automation tasks."""

import os

from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QRadioButton, QDialog
from PyQt5 import QtCore

#Model
from model.contract.contract_template.contract_template_model import Contract_Template_Model
from model.contract.contract_template.contract_template_main import Contract_Template_Main
from model.contract.contract_template.debit_credit_main import Debit_Credit_Main
from model.contract.contract_validation.contract_preval_step1_main import Contract_Preval_Step1_Main
from model.contract.contract_validation.contract_preval_step3_main import Contract_Preval_Step3_Main
from common.common_model import Common_Model

class Contract_Template_Controller():

	def __init__(self, QMainWindow, app_model):

		self._parent = QMainWindow
		self._app_model = app_model
		self._ct_model = Contract_Template_Model(self._parent)
		self._com_model = Common_Model()

		self._dia_ct_response = False

		self._template_op = {
			'isContractTypeTemp': False,
			'isDebitCredit': False,
			'isContractStep1': False,
			'isContractStep3': False
		}

		self._progress_op = {
			True: self._progress_on, 
			False: self._progress_off
		}

		# Toggle Progress display

		self._progress_toggle()

		self._setupConnections()


	def _setupConnections(self):

		#========Contract Type Template Dialog =========#

		self._ct_model.dialog_ui.btnOutputFolder.clicked.connect(self._updateOutputFolder)
		self._ct_model.dialog_ui.btnGenerate.clicked.connect(self._generateTemplate)

	#======================= PROGRESS TOGGLE MODE =================================

	def _progress_toggle(self):
		self._progress_op[self._dia_ct_response]()
		self._ct_model.dialog_ui._lblProgress.setVisible(self._dia_ct_response)
		self._ct_model.dialog_ui._progressBar.setVisible(self._dia_ct_response)

	def _progress_on(self):

		try: self._ct_model.dialog_ui.btnGenerate.disconnect()
		except Exception: pass

		self._ct_model.dialog_ui.btnGenerate.clicked.connect(self._cancelProgram)
		self._ct_model.dialog_ui.btnGenerate.setText('Cancel')

	def _progress_off(self):

		self._ct_model.dialog_ui.btnGenerate.setText('Generate')

	def _updateProgressLabel(self, value):
		self._ct_model.dialog_ui._lblProgress.setText(value)

	def _updateProgressBar(self, value):
		self._ct_model.dialog_ui._progressBar.setValue(value)

	def _cancelProgram(self):

		title = 'Cancel operation'
		msg = 'Are you sure you want to cancel?'
		
		reply = self._ct_model.showDialog('question', title, msg, None, None, True)

		if reply == QMessageBox.Yes:

			if self._template_op['isContractTypeTemp']:
				self.ct_main._cancel_flg = True
			elif self._template_op['isDebitCredit']:
				self.dc_main._cancel_flg = True
			elif self._template_op['isContractStep1']:
				self.cv1_main._cancel_flg = True
			else:
				self.cv3_main._cancel_flg = True
			

	#======================= RADIO BUTTONS TOGGLE MODE =================================

	def _button_toggle(self, display):
		self._ct_model.dialog_ui.rbtnDebit.setVisible(display)
		self._ct_model.dialog_ui.rbtnCredit.setVisible(display)
		self._ct_model.dialog_ui.rbtnAll.setVisible(display)

	#======================= MAIN FUNCTIONS =================================

	def _updateSourceFolder(self):

		try: 
			self._ct_model.dialog_ui.btnSourceFolder.disconnect()
		except Exception: pass

		starting_dir = self._ct_model.dialog_ui.leSourceFolder.text()

		if self._template_op['isContractTypeTemp'] or self._template_op['isContractStep1']:

			path = self._com_model._fileDialog(starting_dir, True, '')
			abs_path = os.path.abspath(path)		
		else:
			path = self._com_model._fileDialog(starting_dir, True, '', True)
			abs_path = os.path.abspath(path)

		self._ct_model.dialog_ui.btnSourceFolder.clicked.connect(self._updateSourceFolder)
		
		self._ct_model.dialog_ui.leSourceFolder.setText(abs_path)

	def _updateOutputFolder(self):

		starting_dir = self._ct_model.dialog_ui.leOutputFolder.text()
		
		path = self._com_model._fileDialog(starting_dir, True, '', True)
		abs_path = os.path.abspath(path)

		self._ct_model.dialog_ui.leOutputFolder.setText(abs_path)

	########################### Contract Templates ##############################

	def _showContractTypeTemplate(self):

		# Update Window Title
		
		self._ct_model.dialog_ui.updateWindowTitle(self._ct_model.Dialog, "Contract Type Template")

		# Clear Template list

		self._ct_model.dialog_ui.leKeyword.setText("")

		# Load settings

		settings_data = self._app_model.parse_config('settings.json')
		self._com_model._load_settings('ContractTypeTemplate', settings_data, self._ct_model.dialog_ui.leSourceFolder, self._ct_model.dialog_ui.leOutputFolder)


		# Update selection

		self._template_op['isContractTypeTemp'] = True
		self._template_op['isDebitCredit'] = False
		self._template_op['isContractStep1'] = False
		self._template_op['isContractStep3'] = False

		# Hide Radio Buttons

		self._button_toggle(False)

		# set connection for Source folder

		self._ct_model.dialog_ui.btnSourceFolder.clicked.connect(self._updateSourceFolder)
		
		response = self._ct_model.Dialog.exec()

		if response == self._ct_model.Dialog.Accepted:
			pass
		else:
			self._ct_model.Dialog.accept()

			#Save settings to settings.json

			src_folder = self._ct_model.dialog_ui.leSourceFolder.text()
			output_folder = self._ct_model.dialog_ui.leOutputFolder.text()

			self._com_model._save_settings('ContractTypeTemplate', src_folder, output_folder)

	def _showDebitCreditTemplate(self):

		# Update Window Title
		
		self._ct_model.dialog_ui.updateWindowTitle(self._ct_model.Dialog, "Debit Credit Template")
		self._ct_model.dialog_ui.lblSource.setText("Source Folder:")

		# Clear Template list

		self._ct_model.dialog_ui.leKeyword.setText("")

		# Load settings

		settings_data = self._app_model.parse_config('settings.json')
		self._com_model._load_settings('DebitCreditTemplate', settings_data, self._ct_model.dialog_ui.leSourceFolder, self._ct_model.dialog_ui.leOutputFolder)

		# Update selection

		self._template_op['isContractTypeTemp'] = False
		self._template_op['isDebitCredit'] = True
		self._template_op['isContractStep1'] = False
		self._template_op['isContractStep3'] = False

		# Show Radio Buttons

		self._button_toggle(True)

		# set connection for Source folder

		self._ct_model.dialog_ui.btnSourceFolder.clicked.connect(self._updateSourceFolder)

		response = self._ct_model.Dialog.exec()

		if response == self._ct_model.Dialog.Accepted:
			pass
		else:
			self._ct_model.Dialog.accept()

		#Save settings to settings.json

			src_folder = self._ct_model.dialog_ui.leSourceFolder.text()
			output_folder = self._ct_model.dialog_ui.leOutputFolder.text()

			self._com_model._save_settings('DebitCreditTemplate', src_folder, output_folder)

	########################### Contract Validations ##############################

	def _showContractPreValStep1Template(self):

		# Update Window Title
		
		self._ct_model.dialog_ui.updateWindowTitle(self._ct_model.Dialog, "Contract Type PreVal Step 1 Template")

		# Clear Template list

		self._ct_model.dialog_ui.leKeyword.setText("")

		# Load settings

		settings_data = self._app_model.parse_config('settings.json')
		self._com_model._load_settings('ContractStep1Template', settings_data, self._ct_model.dialog_ui.leSourceFolder, self._ct_model.dialog_ui.leOutputFolder)

		# Update selection

		self._template_op['isContractTypeTemp'] = False
		self._template_op['isDebitCredit'] = False
		self._template_op['isContractStep1'] = True
		self._template_op['isContractStep3'] = False

		# Hide Radio Buttons

		self._button_toggle(False)

		# set connection for Source folder

		self._ct_model.dialog_ui.btnSourceFolder.clicked.connect(self._updateSourceFolder)
		
		response = self._ct_model.Dialog.exec()

		if response == self._ct_model.Dialog.Accepted:
			pass
		else:
			self._ct_model.Dialog.accept()

			#Save settings to settings.json

			src_folder = self._ct_model.dialog_ui.leSourceFolder.text()
			output_folder = self._ct_model.dialog_ui.leOutputFolder.text()

			self._com_model._save_settings('ContractStep1Template', src_folder, output_folder)

	def _showContractPreValStep3Template(self):

		# Update Window Title
		
		self._ct_model.dialog_ui.updateWindowTitle(self._ct_model.Dialog, "Contract Type PreVal Step 3 Template")

		# Clear Template list

		self._ct_model.dialog_ui.leKeyword.setText("")

		# Load settings

		settings_data = self._app_model.parse_config('settings.json')
		self._com_model._load_settings('ContractStep3Template', settings_data, self._ct_model.dialog_ui.leSourceFolder, self._ct_model.dialog_ui.leOutputFolder)

		# Update selection

		self._template_op['isContractTypeTemp'] = False
		self._template_op['isDebitCredit'] = False
		self._template_op['isContractStep1'] = False
		self._template_op['isContractStep3'] = True

		# Hide Radio Buttons

		self._button_toggle(False)

		# set connection for Source folder

		self._ct_model.dialog_ui.btnSourceFolder.clicked.connect(self._updateSourceFolder)
		
		response = self._ct_model.Dialog.exec()

		if response == self._ct_model.Dialog.Accepted:
			pass
		else:
			self._ct_model.Dialog.accept()

			#Save settings to settings.json

			src_folder = self._ct_model.dialog_ui.leSourceFolder.text()
			output_folder = self._ct_model.dialog_ui.leOutputFolder.text()

			self._com_model._save_settings('ContractStep3Template', src_folder, output_folder)

	def _generateTemplate(self):

		self.keyword = self._ct_model.dialog_ui.leKeyword.text()
		self.src_file = self._ct_model.dialog_ui.leSourceFolder.text()
		self.tgt_folder = self._ct_model.dialog_ui.leOutputFolder.text()

		if self.keyword:

			if self._template_op['isContractTypeTemp']:

				#Notify user of missing template

				folder_path = os.getcwd() + "\\resources\\" + self._ct_model._ct_config['TemplateFolder']
				template_name = self._ct_model._ct_config['ContractTypeName']
				template_fname = folder_path + '\\' + template_name

				template_exist = self._ct_model.checkContractTypeTemplate(folder_path, template_name)

				if template_exist:

					#Read source file to DF

					ct_file_name = '{}_{}.csv'.format(self._ct_model._ct_config['SourceFileName'],self.keyword)
					src_file_name = self.src_file.split('\\')[-1]

					if src_file_name == ct_file_name:

						self._dia_ct_response = True

						# Show the Progress Layout
						self._progress_toggle()

						# Set max value for progress bar
						self._ct_model.dialog_ui._progressBar.setMaximum(5)

						self.ct_main = Contract_Template_Main(template_fname, self.src_file, self.tgt_folder, self.keyword, self._ct_model, self._com_model)
						self.ct_main.currStatus.connect(self._showErrorDialog)
						self.ct_main.countProgress.connect(self._updateProgressBar)
						self.ct_main.txtProgress.connect(self._updateProgressLabel)
						self.ct_main.isCancel.connect(self._on_finished)
						self.ct_main.finished.connect(self._on_finished)
						self.ct_main.start()


					else:

						self._ct_model.showDialog('warning', 'Contract Type Template', 'Invalid Source File Name\n{}'.format(src_file_name), None, None) 
				else:

					self._ct_model.showDialog('warning', 'Contract Type Template', 'Contract Type Template not found.', None, None) 


			elif self._template_op['isDebitCredit']:

				# Get Selection

				selected = self._getSelection()

				# Check Template

				folder_path = os.getcwd() + "\\resources\\" + self._ct_model._dc_config['TemplateFolder']

				tup_template = self._ct_model.checkDebitCreditTemplate(folder_path, selected)
				l_missing = tup_template[1]

				if not l_missing:

					# Check Source Files

					tup_source = self._ct_model.checkDebitCreditSource(self.keyword, self.src_file, selected)
					l_missing_src = tup_source[1]

					if not l_missing_src:

						l_template = tup_template[0]
						l_details = tup_source[0]

						self._dia_ct_response = True

						# Show the Progress Layout
						self._progress_toggle()

						# Set max value for progress bar

						max_cnt = ((len(l_details) *  4) * len(l_template)) + 2
						self._ct_model.dialog_ui._progressBar.setMaximum(max_cnt)

						self.dc_main = Debit_Credit_Main(self.keyword, self.tgt_folder, l_template, l_details, self._ct_model, self._com_model)
						self.dc_main.currStatus.connect(self._showErrorDialog)
						self.dc_main.countProgress.connect(self._updateProgressBar)
						self.dc_main.txtProgress.connect(self._updateProgressLabel)
						self.dc_main.isCancel.connect(self._on_finished)
						self.dc_main.finished.connect(self._on_finished)
						self.dc_main.start()

					else:

						temp_missing = ''
						
						for t,s,f in l_missing_src:

							temp_missing = temp_missing + '{} : {} - {}\n'.format(t,s,f)

						self._ct_model.showDialog('warning', 'Debit Credit Template', 'Source File Not Found:\n {}'.format(temp_missing), None, None)

				else:

					temp_missing = ''
					
					for t,f in l_missing:

						temp_missing = temp_missing + '{}\n'.format(f)

					self._ct_model.showDialog('warning', 'Debit Credit Template', 'Templates Not Found:\n {}'.format(temp_missing), None, None) 

			elif self._template_op['isContractStep1']:

				#Notify user of missing template

				folder_path = os.getcwd() + "\\resources\\" + self._ct_model._cv1_config['TemplateFolder']
				template_name = self._ct_model._cv1_config['PrevalStep1TempName']
				template_fname = folder_path + '\\' + template_name

				template_exist = self._ct_model.checkContractTypeTemplate(folder_path, template_name)

				if template_exist:

					#Read source file to DF

					ct_file_name = '{}_{}.csv'.format(self._ct_model._cv1_config['PrevalStep1SourceFileName'],self.keyword)
					src_file_name = self.src_file.split('\\')[-1]

					if src_file_name == ct_file_name:

						self._dia_ct_response = True

						# Show the Progress Layout
						self._progress_toggle()

						# Set max value for progress bar
						self._ct_model.dialog_ui._progressBar.setMaximum(5)

						self.cv1_main = Contract_Preval_Step1_Main(template_fname, self.src_file, self.tgt_folder, self.keyword, self._ct_model, self._com_model)
						self.cv1_main.currStatus.connect(self._showErrorDialog)
						self.cv1_main.countProgress.connect(self._updateProgressBar)
						self.cv1_main.txtProgress.connect(self._updateProgressLabel)
						self.cv1_main.isCancel.connect(self._on_finished)
						self.cv1_main.finished.connect(self._on_finished)
						self.cv1_main.start()


					else:

						self._ct_model.showDialog('warning', 'Contract Type PreVal Step 1 Template', 'Invalid Source File Name\n{}'.format(src_file_name), None, None) 
				
				else:

					self._ct_model.showDialog('warning', 'Contract Type PreVal Step 1 Template', 'Contract Type PreVal Step 1 Template not found.', None, None) 


			else:

				#Notify user of missing template

				folder_path = os.getcwd() + "\\resources\\" + self._ct_model._cv3_config['TemplateFolder']
				template_name = self._ct_model._cv3_config['PrevalStep3TempName']
				template_fname = folder_path + '\\' + template_name

				template_exist = self._ct_model.checkContractTypeTemplate(folder_path, template_name)

				if template_exist:

					# Check Source Files

					tup_source = self._ct_model.checkContractPreValStep3Source(self.keyword, self.src_file)
					l_missing_src = tup_source[1]

					if not l_missing_src:

						l_details = tup_source[0]

						self._dia_ct_response = True

						# Show the Progress Layout
						self._progress_toggle()

						# Set max value for progress bar

						max_cnt = ((len(l_details) *  4)) + 2
						self._ct_model.dialog_ui._progressBar.setMaximum(max_cnt)

						self.cv3_main = Contract_Preval_Step3_Main(self.keyword, template_fname, self.tgt_folder, l_details, self._ct_model, self._com_model)
						self.cv3_main.currStatus.connect(self._showErrorDialog)
						self.cv3_main.countProgress.connect(self._updateProgressBar)
						self.cv3_main.txtProgress.connect(self._updateProgressLabel)
						self.cv3_main.isCancel.connect(self._on_finished)
						self.cv3_main.finished.connect(self._on_finished)
						self.cv3_main.start()

					else:

						temp_missing = ''
						
						for s,f in l_missing_src:

							temp_missing = temp_missing + '{} - {}\n'.format(s,f)

						self._ct_model.showDialog('warning', 'Contract Type PreVal Step 3 Template', 'Source File Not Found:\n {}'.format(temp_missing), None, None)

				else:

					self._ct_model.showDialog('warning', 'Contract Type PreVal Step 3 Template', 'Contract Type PreVal Step 3 Template not found.', None, None) 



		else:

			# Display Dialog 

			self._ct_model.showDialog('warning', 'No Keyword', 'Please enter a valid keyword', None, None)  

	def _getSelection(self):

		boxElements = self._ct_model.dialog_ui.groupBox_2.children()

		radioButtons = [elem for elem in boxElements if isinstance(elem, QRadioButton)]

		for rb in radioButtons:
			if rb.isChecked():
				checkedOnRb = rb.text()

		selected = checkedOnRb.split('-')[0].strip()

		return selected

	def _on_finished(self):

		self._back_to_default()

		if self._template_op['isContractTypeTemp']:

			if not self.ct_main._cancel_flg and self.ct_main.is_successful:

				self._ct_model.showDialog('inform','Contract Type Template', '{} file successfully saved.'.format(self.ct_main.output_filenm), None, None)

		elif self._template_op['isDebitCredit']:

			if not self.dc_main._cancel_flg and self.dc_main.is_successful:

				self._ct_model.showDialog('inform','Debit Credit Enrichment Template', '{} file successfully saved.'.format(self.dc_main.output_filenm), None, None)

		elif self._template_op['isContractStep1']:

			if not self.cv1_main._cancel_flg and self.cv1_main.is_successful:

				self._ct_model.showDialog('inform','Contract Type PreVal Step 1 Template', '{} file successfully saved.'.format(self.cv1_main.output_filenm), None, None)

		elif self._template_op['isContractStep3']:

			if not self.cv3_main._cancel_flg and self.cv3_main.is_successful:

				self._ct_model.showDialog('inform','Contract Type PreVal Step 3 Template', '{} file successfully saved.'.format(self.cv3_main.output_filenm), None, None)

		else:

			pass


	def _showErrorDialog(self, value):

		if value[1] == 'Load Source':
			self._ct_model.showDialog('warning', 'Warning', 
			'Failed to load source file for keyword ' + value[0] + ' to a dataframe.', 'See details for more info.', value[2])
		elif value[1] == 'Load Template':
			self._ct_model.showDialog('error', 'Error', 
			'Failed to load the Pricing Template File for ' + value[0] + ' to a dataframe.', 'See details for more info.', value[2])
		elif value[1] == 'Populate Worksheet':
			self._ct_model.showDialog('error', 'Error', 
			'Failed to populate worksheet ' + value[0] + '.', 'See details for more info.', value[2])
		elif value[1] == 'Save Template':
			self._ct_model.showDialog('error', 'Error', 
			'Failed to save template to ' + value[0] + '.', None, value[2])

	def _back_to_default(self):

		self._dia_ct_response = False

		# Set default valud of Progress Bar
		self._updateProgressBar(0)
		
		try: self._ct_model.dialog_ui.btnGenerate.disconnect()
		except Exception: pass
		self._ct_model.dialog_ui.btnGenerate.clicked.connect(self._generateTemplate)
		
		self._progress_toggle()