#!/usr/bin/env python3

# Filename: pricing_validation_main.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os
import pandas as pd
import xlsxwriter

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QMessageBox

#Model
from model.pricing.pricing_validation.pricing_validation_model import Pricing_Validation_Model
from common.common_model import Common_Model

class Pricing_Validation_Main(QThread):

	"""
	Runs in thread.
	"""

	txtProgress = pyqtSignal(str)
	countProgress = pyqtSignal(int)
	currStatus = pyqtSignal(list)

	def __init__(self, src_folder, tgt_folder, keyword, templates, pt_model):
		super(Pricing_Validation_Main, self).__init__()

		self._src_folder = src_folder
		self._tgt_folder = tgt_folder
		self._keyword = keyword
		self._l_templates = templates
		self._pt_model = pt_model
		self._common_mod = Common_Model()
		self._pv_model = Pricing_Validation_Model(self._common_mod, self._pt_model)
		
		self.timer = QTime()
		self.elapsed_time = None

		self.is_running = True
		self._progress_count = 0
		self._abort_flg = False
		self._cancel_flg = False
		self._main_dir = os.getcwd()
		
		self.preval_price_df = None

	def run(self):

		''' 
		Read source file to DataFrame and Excel file (for validation)
		Filter dataframe per Usage Type
		Perform Mappings
		Populate the validated dataframe to template
		'''

		# Start timer
		
		self.timer.start()
		
		self.txtProgress.emit('Loading source file to dataframes.')

		success = False
		while not success:
			try:

				df_price_all = self._pv_model.read_source_to_DF(self._keyword, self._src_folder, 'Pricing')
				df_scales_all = self._pv_model.read_source_to_DF(self._keyword, self._src_folder,  'Scales')
				df_minf_all = self._pv_model.read_source_to_DF(self._keyword, self._src_folder,  'MINF')

				success = True
			except Exception as e:

				self.currStatus.emit([self._keyword,'Load Source',str(e)])

				response = None
				while response is None:
					response = self._pt_model.replyBtn
					time.sleep(1)

				if response == QMessageBox.Close:
					self._abort_flg = True
					self._pt_model.replyBtn = None
					success = True

		if not self._abort_flg:

		#Loop on the templates found

			for i in self._l_templates:

				usage_type = i[0]

				wb_name = 'OTC_{}_Pricing_Pre_Validation_Report_{}.xlsx'.format(usage_type, self._keyword.upper())
				output_filenm = self._tgt_folder + "\\" + wb_name

				# Create a Pandas Excel writer using XlsxWriter as the engine.
				writer = pd.ExcelWriter(output_filenm, engine='xlsxwriter', options={'strings_to_numbers': False})

				# Get the xlsxwriter workbook and worksheet objects.
				workbook  = writer.book

				#Set workbook formats

				self._common_mod.set_workbook_formats(workbook)

				l_price_tabs = [{'Price': {'Template_Sheet_Name': 'Customer prices', 'Template_Mapping_Index': 4, 'Template_Column_Index': 9, 'Chart_Sheeet_Name': 'Pricing_Summary', 'Details_Sheet_Name': 'Price_PreValidation_Details'}},
								{'Scale': {'Template_Sheet_Name': 'Customer scale price', 'Template_Mapping_Index': 4, 'Template_Column_Index': 8, 'Chart_Sheeet_Name': 'Scales_Summary', 'Details_Sheet_Name': 'Scales_PreValidation_Details'}},
								{'MINF': {'Template_Sheet_Name': 'MINF Details MTable', 'Template_Mapping_Index': 1, 'Template_Column_Index': 6, 'Chart_Sheeet_Name': 'MINF_Summary', 'Details_Sheet_Name': 'MINF_PreValidation_Details'}}]

				for d_tab in l_price_tabs:

					for k,v in d_tab.items():

						tab = k
						template_sheet_name = v['Template_Sheet_Name']
						template_mapping_idx = v['Template_Mapping_Index']
						template_column_idx = v['Template_Column_Index']
						chart_sheet_name = v['Chart_Sheeet_Name']
						details_sheet_name = v['Details_Sheet_Name']

						self.txtProgress.emit('Started: Processing {} - Initializing {} DataFrame.'.format(usage_type, tab))

						#Filter dataframe

						if tab == 'Price':
							preval_df = df_price_all[df_price_all['USAGE_TYPE_CD'] == usage_type]
						elif tab == 'Scale':
							preval_df = df_scales_all[df_scales_all['USAGE_TYPE_CD'] == usage_type]
						else:
							preval_df = df_minf_all[df_minf_all['USAGE_TYPE_CD'] == usage_type]

						#Initialize Pricing dataframe 

						preval_df = self._pv_model.initialize_preval_df(preval_df, tab)

						self.txtProgress.emit('Finished: Processing {} - Initializing {} DataFrame.'.format(usage_type, tab))
						time.sleep(3)

						#Read Template columns for mapping

						self.txtProgress.emit('Started: Processing {} - Get {} Template Column Mappings.'.format(usage_type,tab))

						template_columns = self._pv_model.get_template_mappings(usage_type, template_sheet_name, template_mapping_idx)

						self.txtProgress.emit('Started: Processing {} - Get {} Template Column Mappings.'.format(usage_type,tab))
						time.sleep(3)

						#Generate Price template DF

						self.txtProgress.emit('Started: Processing {} - Generating {} Template DataFrame.'.format(usage_type,tab))

						if tab == 'Price':
							self.preval_price_df = preval_df.copy()
							template_df = self._pv_model.generate_template_df(usage_type, preval_df, template_columns, template_column_idx, tab)
						else:
							template_df = self._pv_model.generate_template_df(usage_type, preval_df, template_columns, template_column_idx, tab, self.preval_price_df)
						self.txtProgress.emit('Finished: Processing {} - Generating {} Template DataFrame.'.format(usage_type,tab))
						time.sleep(3)
						
						#Populate Summary Chart

						self.txtProgress.emit('Started: Processing {} - Populating {} Summary Chart.'.format(usage_type,tab))

						self._pv_model.populate_summary_chart(usage_type, workbook, template_df, chart_sheet_name, template_column_idx)

						self.txtProgress.emit('Finished: Processing {} - Populating {} Summary Chart.'.format(usage_type,tab))
						time.sleep(3)

						#Populate Details sheet

						self.txtProgress.emit('Started: Processing {} - Populating {} Details Sheet.'.format(usage_type,tab))

						self._pv_model.populate_details_worksheet(writer, template_df, details_sheet_name, template_column_idx)

						self.txtProgress.emit('Finished: Processing {} - Populating {} Details Sheet.'.format(usage_type,tab))
						time.sleep(3)


				# ###################### PRICE TAB ########################

				# self.txtProgress.emit('Started: Processing {} - Initializing Pricing DataFrame.'.format(usage_type))

				# #Filter dataframe

				# preval_price_df = df_price_all[df_price_all['USAGE_TYPE_CD'] == usage_type]

				# #Initialize Pricing dataframe 

				# preval_price_df = self._pv_model.initialize_preval_df(preval_price_df, 'Price')

				# self.txtProgress.emit('Finished: Processing {} - Initializing Pricing DataFrame.'.format(usage_type))
				# time.sleep(3)

				# #Read Template columns for mapping

				# self.txtProgress.emit('Started: Processing {} - Get Pricing Template Column Mappings.'.format(usage_type))

				# template_columns = self._pv_model.get_template_mappings(usage_type, 'Customer prices', 4)

				# self.txtProgress.emit('Started: Processing {} - Get Pricing Template Column Mappings.'.format(usage_type))
				# time.sleep(3)

				# #Generate Price template DF

				# self.txtProgress.emit('Started: Processing {} - Generating Pricing Template DataFrame.'.format(usage_type))

				# price_df = self._pv_model.generate_template_df(usage_type, preval_price_df, template_columns, 9, 'Price')

				# self.txtProgress.emit('Finished: Processing {} - Generating Pricing Template DataFrame.'.format(usage_type))
				# time.sleep(3)

				# wb_name = 'OTC_{}_Pricing_Pre_Validation_Report_{}.xlsx'.format(usage_type, self._keyword.upper())
				# output_filenm = self._tgt_folder + "\\" + wb_name

				# # Create a Pandas Excel writer using XlsxWriter as the engine.
				# writer = pd.ExcelWriter(output_filenm, engine='xlsxwriter', options={'strings_to_numbers': False})

				# # Get the xlsxwriter workbook and worksheet objects.
				# workbook  = writer.book

				# #Set workbook formats

				# self._common_mod.set_workbook_formats(workbook)

				# #Populate Summary Chart

				# self.txtProgress.emit('Started: Processing {} - Populating Pricing Summary Chart.'.format(usage_type))

				# self._pv_model.populate_summary_chart(usage_type, workbook, price_df, 'Pricing_Summary', 9)

				# self.txtProgress.emit('Finished: Processing {} - Populating Pricing Summary Chart.'.format(usage_type))
				# time.sleep(3)

				# #Populate Details sheet

				# self.txtProgress.emit('Started: Processing {} - Populating Pricing Details Sheet.'.format(usage_type))

				# sheet_name = 'Pricing_PreValidation_Details'
				# self._pv_model.populate_details_worksheet(writer, price_df, sheet_name, 9)

				# self.txtProgress.emit('Finished: Processing {} - Populating Pricing Details Sheet.'.format(usage_type))
				# time.sleep(3)


				# ###################### SCALES TAB ########################

				# self.txtProgress.emit('Started: Processing {} - Initializing Scales DataFrame.'.format(usage_type))

				# #Filter dataframe

				# preval_scales_df = df_scales_all[df_scales_all['USAGE_TYPE_CD'] == usage_type]

				# #Initialize Pricing dataframe 

				# preval_scales_df = self._pv_model.initialize_preval_df(preval_scales_df, 'Scales')

				# self.txtProgress.emit('Finished: Processing {} - Initializing Scales DataFrame.'.format(usage_type))
				# time.sleep(3)

				# #Read Template columns for mapping

				# self.txtProgress.emit('Started: Processing {} - Get Scales Template Column Mappings.'.format(usage_type))

				# template_columns = self._pv_model.get_template_mappings(usage_type, 'Customer scale price', 4)

				# self.txtProgress.emit('Started: Processing {} - Get Scales Template Column Mappings.'.format(usage_type))
				# time.sleep(3)

				# #Generate Scales template DF

				# self.txtProgress.emit('Started: Processing {} - Generating Scales Template DataFrame.'.format(usage_type))

				# scales_df = self._pv_model.generate_template_df(usage_type, preval_scales_df, template_columns, 8, 'Scales', preval_price_df)

				# self.txtProgress.emit('Finished: Processing {} - Generating Scales Template DataFrame.'.format(usage_type))
				# time.sleep(3)

				# #Populate Summary Chart

				# self.txtProgress.emit('Started: Processing {} - Populating Scales Summary Chart.'.format(usage_type))

				# self._pv_model.populate_summary_chart(usage_type, workbook, scales_df, 'Scales_Summary', 8)

				# self.txtProgress.emit('Finished: Processing {} - Populating Scales Summary Chart.'.format(usage_type))
				# time.sleep(3)

				# #Populate Details sheet

				# self.txtProgress.emit('Started: Processing {} - Populating Scales Details Sheet.'.format(usage_type))

				# sheet_name = 'Scales_PreValidation_Details'
				# self._pv_model.populate_details_worksheet(writer, scales_df, sheet_name, 8)

				# self.txtProgress.emit('Finished: Processing {} - Populating Scales Details Sheet.'.format(usage_type))
				# time.sleep(3)

				# print(self._pt_model._templates)

				# ###################### MINF TAB ########################

				# self.txtProgress.emit('Started: Processing {} - Initializing MINF DataFrame.'.format(usage_type))

				# #Filter dataframe

				# preval_minf_df = df_minf_all[df_minf_all['USAGE_TYPE_CD'] == usage_type]

				# #Initialize Pricing dataframe 

				# preval_minf_df = self._pv_model.initialize_preval_df(preval_minf_df, 'MINF')

				# self.txtProgress.emit('Finished: Processing {} - Initializing MINF DataFrame.'.format(usage_type))
				# time.sleep(3)

				# #Read Template columns for mapping

				# self.txtProgress.emit('Started: Processing {} - Get MINF Template Column Mappings.'.format(usage_type))

				# template_columns = self._pv_model.get_template_mappings(usage_type, 'MINF Details MTable', 1)

				# self.txtProgress.emit('Started: Processing {} - Get MINF Template Column Mappings.'.format(usage_type))
				# time.sleep(3)

				# #Generate MINF template DF

				# self.txtProgress.emit('Started: Processing {} - Generating MINF Template DataFrame.'.format(usage_type))

				# minf_df = self._pv_model.generate_template_df(usage_type, preval_minf_df, template_columns, 6, 'MINF', preval_price_df)

				# self.txtProgress.emit('Finished: Processing {} - Generating MINF Template DataFrame.'.format(usage_type))
				# time.sleep(3)

				# #Populate Summary Chart

				# self.txtProgress.emit('Started: Processing {} - Populating MINF Summary Chart.'.format(usage_type))

				# self._pv_model.populate_summary_chart(usage_type, workbook, minf_df, 'MINF_Summary', 6)

				# self.txtProgress.emit('Finished: Processing {} - Populating MINF Summary Chart.'.format(usage_type))
				# time.sleep(3)

				# #Populate Details sheet

				# self.txtProgress.emit('Started: Processing {} - Populating MINF Details Sheet.'.format(usage_type))

				# sheet_name = 'MINF_PreValidation_Details'
				# self._pv_model.populate_details_worksheet(writer, minf_df, sheet_name, 6)

				# self.txtProgress.emit('Finished: Processing {} - Populating MINF Details Sheet.'.format(usage_type))
				# time.sleep(3)

				print(self._pt_model._templates)

				#Save Workbook

				self.txtProgress.emit('Started: Processing {} - Saving Workbook to Output folder.'.format(usage_type))

				writer.save()

				self.txtProgress.emit('Finished: Processing {} - Saving Workbook to Output folder.'.format(usage_type))
				time.sleep(3)