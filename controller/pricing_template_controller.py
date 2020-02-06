#!/usr/bin/env python3

# Filename: pricing_template_controller.py

"""This app is for the Amadeus automation tasks."""

import os

from PyQt5.QtWidgets import QListWidgetItem, QMessageBox, QRadioButton, QDialog
from PyQt5 import QtCore

#Model
from model.pricing.pricing_template.pricing_template_model import Pricing_Template_Model
from model.pricing.pricing_template.pricing_template_main import Pricing_Template_Main
from model.pricing.pricing_validation.pricing_validation_main import Pricing_Validation_Main
from common.common_model import Common_Model

class Pricing_Template_Controller():

	def __init__(self, QMainWindow, app_model):

		self._parent = QMainWindow
		self._app_model = app_model
		self._pt_model = Pricing_Template_Model(self._parent)
		self._com_model = Common_Model()

		self._ut_dup_bool = False
		self._selected = None
		self._continue_flag = True
		self._dia_pt_response = False

		self._selected_op = {
			'isPricingTemp': False,
			'isPricingVal': False
		}

		self._progress_op = {
			True: self._progress_on, 
			False: self._progress_off
		}


		# set connects for pricing template

		self._setupConnections()

		# Toggle Progress display

		self._progress_toggle()

	def _setupConnections(self):

	    #========Pricing Template Dialog =========#

	    self._pt_model.dialog_ui._cbUsageFlows.activated[int].connect(self._usageflow_changed)
	    self._pt_model.dialog_ui._btnChangeSrc.clicked.connect(self._updateSourceFolder)
	    self._pt_model.dialog_ui._btnChangeOut.clicked.connect(self._updateOutputFolder)
	    self._pt_model.dialog_ui._btnGenerate.clicked.connect(self._showSelection)
	    self._pt_model.dialog_ui._btnDelete.clicked.connect(self._deleteUsageFlow)
	    self._pt_model.dialog_warn_ui._btnBox.accepted.connect(self._dialog_warn_accept)
	    self._pt_model.dialog_warn_ui._btnBox.rejected.connect(self._dialog_warn_reject)

	    #========Pricing Template Finish Dialog =========#

	    self._pt_model.Dialog_fin_ui._btnReport.clicked.connect(self._display_pricing_template_report)
	    self._pt_model.Dialog_fin_ui._btnClose.clicked.connect(self._dialog_finish_close)

	    #========Pricing Template Report Dialog =========#

	    self._pt_model.Dialog_report_ui._btnClose.clicked.connect(self._dialog_report_close)

	    #========Pricing Template Select Dialog =========#

	    self._pt_model.Dialog_select_ui.buttonBox.accepted.connect(self._getSelection)
	    self._pt_model.Dialog_select_ui.buttonBox.rejected.connect(self._closeSelectDialog)

	def _updateSourceFolder(self):

		starting_dir = self._pt_model.dialog_ui._leSourceFolder.text()

		path = self._com_model._fileDialog(starting_dir, True, '', True)
		abs_path = os.path.abspath(path)

		self._pt_model.dialog_ui._leSourceFolder.setText(abs_path)

	def _updateOutputFolder(self):

		starting_dir = self._pt_model.dialog_ui._leOutputFolder.text()

		path = self._com_model._fileDialog(starting_dir, True, '', True)
		abs_path = os.path.abspath(path)

		self._pt_model.dialog_ui._leOutputFolder.setText(abs_path)

	def _showPricingTemplate(self):

		# Update Window Title
		
		self._pt_model.dialog_ui.updateWindowTitle(self._pt_model.Dialog, "Pricing Template")

		# Populate Usage Flow combo box

		self._populateUsageFlows()

		# Load settings

		settings_data = self._app_model.parse_config('settings.json')
		self._com_model._load_settings('PricingTemplate', settings_data, self._pt_model.dialog_ui._leSourceFolder, self._pt_model.dialog_ui._leOutputFolder)

		# Clear Template list

		self._pt_model.dialog_ui._leKeyword.setText("")
		self._pt_model.remove_template_list()

		# Update selection

		self._selected_op['isPricingTemp'] = True
		self._selected_op['isPricingVal'] = False
		
		response = self._pt_model.Dialog.exec()

		if response == self._pt_model.Dialog.Accepted:
			pass
		else:
			self._pt_model.Dialog.accept()
			self._pt_model.dialog_ui._lvUsageFlow.clear()

			#Save settings to settings.json

			src_folder = self._pt_model.dialog_ui._leSourceFolder.text()
			output_folder = self._pt_model.dialog_ui._leOutputFolder.text()

			self._com_model._save_settings('PricingTemplate', src_folder, output_folder)

	def _showPricingValidation(self):

		# Update Window Title
		
		self._pt_model.dialog_ui.updateWindowTitle(self._pt_model.Dialog, "Pricing Validation")

		# Populate Usage Flow combo box

		self._populateUsageFlows()

		# Load settings

		settings_data = self._app_model.parse_config('settings.json')
		self._com_model._load_settings('PricingValidation', settings_data, self._pt_model.dialog_ui._leSourceFolder, self._pt_model.dialog_ui._leOutputFolder)

		# Clear Template list

		self._pt_model.dialog_ui._leKeyword.setText("")
		self._pt_model.remove_template_list()

		# Update selection

		self._selected_op['isPricingTemp'] = False
		self._selected_op['isPricingVal'] = True
		
		response = self._pt_model.Dialog.exec()

		if response == self._pt_model.Dialog.Accepted:
			pass
		else:
			self._pt_model.Dialog.accept()
			self._pt_model.dialog_ui._lvUsageFlow.clear()

			#Save settings to settings.json

			src_folder = self._pt_model.dialog_ui._leSourceFolder.text()
			output_folder = self._pt_model.dialog_ui._leOutputFolder.text()

			self._com_model._save_settings('PricingValidation', src_folder, output_folder)

	def _get_usagetype(self):
		''' Returns the currently selection workspace from combobox. '''
		return str(self._pt_model.dialog_ui._cbUsageFlows.currentText())

	def _usageflow_changed(self):
		if self._get_usagetype() == "ALL":
			self._pt_model.dialog_ui._lvUsageFlow.clear()
			self._app_model.delete_usage_types()
		else:
			self._populateUsageTypeList()

	def _add_usage_type(self, usage_type):
		self._app_model.add_usagetype(usage_type)

	def _selectionChanged(self):
		l_selected = []
		l_selected_obj = self._pt_model.dialog_ui._lvUsageFlow.selectedItems()

		for item in l_selected_obj:
			u_type = item.text().split('-')[0].strip()
			l_selected.append(u_type)

		return l_selected

	def _deleteUsageFlow(self):

		l_to_be_deleted = self._selectionChanged()

		for i in l_to_be_deleted:
			self._app_model.remove_usageflow(i)

		l_usage_types = self._app_model.get_usage_types()

		self._refreshUsageTypeList(l_usage_types)

	def _showSelection(self):

		# Display Selection dialog

		if self._get_usagetype() == "ALL":

			self._pt_model.Dialog_select.exec()

		else:

			self._generatePricingTemplate()

	def _getSelection(self):

		boxElements = self._pt_model.Dialog_select_ui.groupBox.children()

		radioButtons = [elem for elem in boxElements if isinstance(elem, QRadioButton)]

		for rb in radioButtons:
			if rb.isChecked():
				checkedOnRb = rb.text()

		self._selected = checkedOnRb.split('-')[0].strip()

		self._closeSelectDialog()
		self._generatePricingTemplate()
		
	def _closeSelectDialog(self):
		self._pt_model.Dialog_select.close()

	def _generatePricingTemplate(self):

		self.keyword = self._pt_model.dialog_ui._leKeyword.text()
		self.src_folder = self._pt_model.dialog_ui._leSourceFolder.text()
		self.tgt_folder = self._pt_model.dialog_ui._leOutputFolder.text()

		if self.keyword:

			#Get Usage Type List

			if self._get_usagetype() == "ALL" and self._selected.upper() == "ALL":
				l_usage_types = self._app_model.get_usageflows()[1:]
			elif self._get_usagetype() == "ALL" and self._selected.upper() is not None:
				l_usage_types = [usage_type for usage_type in self._app_model.get_usageflows()[1:] if usage_type in self._app_model.get_usagetype_by_report_type(self._selected)]
			else:
				l_usage_types = self._app_model.get_usage_types()

			#Get Templates found

			self.l_templates_found = self._pt_model.get_template_list(l_usage_types)

			self.l_templates_not_found = self._pt_model.get_template_list_not_found(l_usage_types)

			if self._continue_flag:

				if len(self.l_templates_found) > 0:

					#Notify user of missing template

					if self.l_templates_not_found:

						self._populate_text_template_logs(self.l_templates_not_found, self._pt_model.dialog_warn_ui._teUsageTypes)
						self._pt_model.Dialog_warn.exec()

					else:

						self._dia_pt_response = True

					# Run the Main Program on Thread

					if self._selected_op['isPricingTemp']:

						# Show the Progress Layout
						self._progress_toggle()

						# Set max value for progress bar
						max_progress_count = len(self.l_templates_found)
						self._pt_model.dialog_ui._progressBar.setMaximum(max_progress_count)

						self.pt_main = Pricing_Template_Main(self.src_folder, self.tgt_folder, self.keyword, self.l_templates_found, self._pt_model)
						self.pt_main.countProgress.connect(self._updateProgressBar)
						self.pt_main.txtProgress.connect(self._updateProgressLabel)
						self.pt_main.currStatus.connect(self._showErrorDialog)
						self.pt_main.finished.connect(self._on_finished)
						self.pt_main.start()
						

					else:
						
						# Show the Progress Layout
						self._progress_toggle()

						# Set max value for progress bar
						max_progress_count = len(self.l_templates_found)
						self._pt_model.dialog_ui._progressBar.setMaximum(max_progress_count)

						self.pv_main = Pricing_Validation_Main(self.src_folder, self.tgt_folder, self.keyword, self.l_templates_found, self._pt_model)
						self.pv_main.countProgress.connect(self._updateProgressBar)
						self.pv_main.txtProgress.connect(self._updateProgressLabel)
						self.pv_main.currStatus.connect(self._showErrorDialog)
						self.pv_main.finished.connect(self._on_finished)
						self.pv_main.start()

				else:

					self._pt_model.showDialog('warning', 'Error - Pricing Template', 
					'No template found for the selected Usage flow(s).', None, None)
				
		else:

			# Display Dialog 

			self._pt_model.showDialog('warning', 'No Keyword', 
			'Please enter a valid keyword', None, None)  

	def _dialog_warn_accept(self):

		self._continue_flag = True
		self._dia_pt_response = True
		self._pt_model.Dialog_warn.close()

	def _dialog_warn_reject(self):

		self._continue_flag = False
		self._dia_pt_response = False

		# Clear template list
		self._pt_model.remove_template_list()

		self._pt_model.Dialog_warn.close()

	def _dialog_report_close(self):

		self._pt_model.Dialog_report.close()
		self._back_to_default()

	def _dialog_finish_close(self):

		self._pt_model.Dialog_finish.close()

	def _cancelProgram(self):

		title = 'Cancel operation'
		msg = 'Are you sure you want to cancel?'
		
		reply = self._pt_model.showDialog('question', title, msg, None, None, True)

		if reply == QMessageBox.Yes:
			self.pt_main._cancel_flg = True

	def _showErrorDialog(self, value):

		if value[1] == 'Load Source':
			self._pt_model.showDialog('warning', 'Warning', 
			'Failed to load source file for keyword ' + value[0] + ' to a dataframe.', 'See details for more info.', value[2])
		elif value[1] == 'Load Template':
			self._pt_model.showDialog('error', 'Error', 
			'Failed to load the Pricing Template File for ' + value[0] + ' to a dataframe.', 'See details for more info.', value[2])
		elif value[1] == 'Populate Worksheet':
			self._pt_model.showDialog('error', 'Error', 
			value[0] + ' - Failed to populate worksheet ' + value[2] + '.', 'See details for more info.', value[3])
		elif value[1] == 'Save Template':
			self._pt_model.showDialog('error', 'Error', 
			value[0] + ' - Failed to save template to ' + value[2] + '.', None, value[3])

	def _on_finished(self):

		if self._selected_op['isPricingTemp']:
			
			if self.pt_main._abort_flg or self.pt_main._cancel_flg:

				#self._pt_model.Dialog.close()
				self._back_to_default()

			else:

				self._display_finish_dialog()
				
		else:

			if self.pv_main._abort_flg or self.pv_main._cancel_flg:

				#self._pt_model.Dialog.close()
				self._back_to_default()
			else:

				self._display_finish_dialog()

		self._back_to_default()

	#======================= PROGRESS TOGGLE MODE =================================

	def _progress_toggle(self):
		self._progress_op[self._dia_pt_response]()
		self._pt_model.dialog_ui._lblProgress.setVisible(self._dia_pt_response)
		self._pt_model.dialog_ui._progressBar.setVisible(self._dia_pt_response)

	def _progress_on(self):

		try: self._pt_model.dialog_ui._btnGenerate.disconnect()
		except Exception: pass

		self._pt_model.dialog_ui._btnGenerate.clicked.connect(self._cancelProgram)
		self._pt_model.dialog_ui._btnGenerate.setText('Cancel')

	def _progress_off(self):

		self._pt_model.dialog_ui._btnGenerate.setText('Generate')

	def _updateProgressLabel(self, value):
		self._pt_model.dialog_ui._lblProgress.setText(value)

	def _updateProgressBar(self, value):
		self._pt_model.dialog_ui._progressBar.setValue(value)


	#==================================== DISPLAY =================================#

	def _populateUsageFlows(self):

		#Add All usage type

		self._app_model.add_usageflow('ALL')

		for u in self._app_model._conf_data['usageFlows']:
			usagetype = u['UsageType']
			self._app_model.add_usageflow(str(usagetype))

		# Populate combobox

		self._pt_model.dialog_ui._cbUsageFlows.clear()
		self._pt_model.dialog_ui._cbUsageFlows.addItems(self._app_model.get_usageflows())

	def _refreshUsageTypeList(self, l_usage_type):

		# Clear List Widget

		self._pt_model.dialog_ui._lvUsageFlow.clear()

		for usage_type in l_usage_type:

			#Add selected item to List Widget
			item = QListWidgetItem(self._pt_model.dialog_ui._lvUsageFlow)
			item.setText(usage_type + ' - ' + self._app_model.get_usage_type_details(usage_type,usage_type)[0])

	def _populateUsageTypeList(self):

		usage_type = self._get_usagetype()

		self._continue_flag = True

		self._ut_dup_bool = self._app_model.check_dup_usage_type(usage_type)

		if not self._ut_dup_bool:

			#Add usage type to OD
			self._add_usage_type(usage_type)

			#Add selected item to List Widget
			item = QListWidgetItem(self._pt_model.dialog_ui._lvUsageFlow)
			item.setText(usage_type + ' - ' + self._app_model.get_usage_type_details(usage_type,usage_type)[0])

		else:

			# Display Dialog 

			self._pt_model.showDialog('inform', 'Usage Type Selection', 
			'Duplicate: ' +usage_type+ ' already added on the list.', None, None)           

	def _generate_pricing_template_report(self):

		cnt_source = self._pt_model.get_template_counts()
		self._pt_model.Dialog_report_ui.widget_Bar.display_result(cnt_source)

	def _generate_pricing_table_report(self):

		model = self._pt_model.get_missing_columns_df()

		self._pt_model.Dialog_report_ui._tblMissingColumns.setModel(model)

		# set horizontal header properties
		hh = self._pt_model.Dialog_report_ui._tblMissingColumns.horizontalHeader()
		hh.setStretchLastSection(True)

		# set column width to fit contents
		self._pt_model.Dialog_report_ui._tblMissingColumns.resizeColumnsToContents()

		# set minimum size
		self._pt_model.Dialog_report_ui._tblMissingColumns.setMinimumSize(QtCore.QSize(0, 200))

		# set row height
		# nrows = len(df.index)
		# for row in xrange(nrows):
		#     tv.setRowHeight(row, 14)

	def _display_finish_dialog(self):

		# Display finish dialog

		if len(self.l_templates_found) == 0:

			self._pt_model.Dialog_fin_ui._btnReport.setEnabled(False)

		#Total complete templates

		cnt = 0 
		for i in self.l_templates_found:

			usage_type = i[0]
			status = self._pt_model.get_template_status(usage_type)

			if status == 'c':
				cnt += 1

		self._pt_model.Dialog_fin_ui._leTotalTemp.setText(str(cnt))
		self._pt_model.Dialog_fin_ui._teOutputFolder.setText(self.tgt_folder)

		if self._selected_op['isPricingTemp']:
			self._pt_model.Dialog_fin_ui._le_TotalTime.setText(self.pt_main.elapsed_time)
		else:
			self._pt_model.Dialog_fin_ui._le_TotalTime.setText(self.pv_main.elapsed_time)

		self._pt_model.Dialog_finish.exec()


	def _display_pricing_template_report(self):

		# Close finish dialog

		self._dialog_finish_close()

		# Generate Report

		self._generate_pricing_template_report()

		# Populate Table

		self._generate_pricing_table_report()

		# Populate List of templates not found

		self._populate_text_template_logs(self.l_templates_not_found, self._pt_model.Dialog_report_ui._te_templates)

		if self._selected_op['isPricingTemp']:

			# Populate List of Missing usage types

			set_usage_type_src = set(self.pt_main.get_all_usage_types())
			set_usage_type_app = set([t['UsageType'] for t in self._app_model._conf_data['usageFlows']])

			l_missing = list(sorted(set_usage_type_src - set_usage_type_app))

			self._populate_text_logs(l_missing, self._pt_model.Dialog_report_ui._te_usagetype)

		# Show Dialog report

		self._pt_model.Dialog_report.exec()

	def _populate_text_logs(self, l_object, te_object):

		if l_object:

			# Clear Line Edit
			te_object.clear()

			for i in l_object:
				te_object.append(i)

	def _populate_text_template_logs(self, l_object, te_object):

		if l_object:

			# Clear Line Edit
			te_object.clear()

			for i in l_object:
				te_object.append(i[0])

	def _back_to_default(self):

		self._continue_flag = True
		self._dia_pt_response = False

		#Clear Selected templates list
		self._pt_model.remove_template_list()

		# Set default valud of Progress Bar
		self._updateProgressBar(0)
		
		try: self._pt_model.dialog_ui._btnGenerate.disconnect()
		except Exception: pass
		self._pt_model.dialog_ui._btnGenerate.clicked.connect(self._showSelection)
		
		self._progress_toggle()