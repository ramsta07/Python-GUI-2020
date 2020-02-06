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

				if self._cancel_flg:break;

				status = self._pt_model.get_template_status(usage_type)

				if status == '':

					wb_name = 'OTC_{}_Pricing_Pre_Validation_Report_{}.xlsx'.format(usage_type, self._keyword.upper())
					output_filenm = self._tgt_folder + "\\" + wb_name

					# Create a Pandas Excel writer using XlsxWriter as the engine.
					writer = pd.ExcelWriter(output_filenm, engine='xlsxwriter', options={'strings_to_numbers': False})

					# Get the xlsxwriter workbook and worksheet objects.
					workbook  = writer.book

					#Set workbook formats

					self._common_mod.set_workbook_formats(workbook)

					l_price_tabs = self._pv_model._config['PricingTabs']

					success = False
					while not success:
						try:

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
										template_df = self._pv_model.generate_template_df(usage_type, preval_df, template_sheet_name, template_columns, template_column_idx, tab)
									elif tab == 'Scale':

										merge_scale_price_df = self._pv_model.merge_scale_price_df(preval_df,self.preval_price_df)
										template_df = self._pv_model.generate_template_df(usage_type, merge_scale_price_df, template_sheet_name, template_columns, template_column_idx, tab, self.preval_price_df)

									else:
										merge_minf_price_df = self._pv_model.merge_minf_price_df(preval_df,self.preval_price_df)
										template_df = self._pv_model.generate_template_df(usage_type, merge_minf_price_df, template_sheet_name, template_columns, template_column_idx, tab, self.preval_price_df)

									self.txtProgress.emit('Finished: Processing {} - Generating {} Template DataFrame.'.format(usage_type,tab))
									time.sleep(3)
									
									#Populate Summary Chart

									self.txtProgress.emit('Started: Processing {} - Populating {} Summary Chart.'.format(usage_type,tab))

									print(template_df.columns.to_list())
									self._pv_model.populate_summary_chart(usage_type, workbook, template_df, chart_sheet_name, template_column_idx)

									self.txtProgress.emit('Finished: Processing {} - Populating {} Summary Chart.'.format(usage_type,tab))
									time.sleep(3)

									#Populate Details sheet

									self.txtProgress.emit('Started: Processing {} - Populating {} Details Sheet.'.format(usage_type,tab))

									self._pv_model.populate_details_worksheet(writer, template_df, details_sheet_name, template_column_idx)

									self.txtProgress.emit('Finished: Processing {} - Populating {} Details Sheet.'.format(usage_type,tab))
									time.sleep(3)

									#Generating Template Counts

									if not self._abort_flg:

										self.txtProgress.emit('Started: Processing {} - Generating Data Counts.'.format(usage_type))

										data = {'Source' : 0, 'Template' : preval_df.shape[0]}
										self._pt_model.append_template_logs(usage_type, 3, tab, data)

										self.txtProgress.emit('Finished: Processing {} - Generating Data Counts.'.format(usage_type))

							success = True

						except Exception as e:

							self.currStatus.emit([usage_type,'Populate Worksheet',tab,str(e)])

							response = None
							while response is None:
								response = self._pt_model.replyBtn
								time.sleep(1)

								if response == QMessageBox.Abort:
									self._abort_flg = True
									self._pt_model.replyBtn = None
									success = True
								elif response == QMessageBox.Retry:
									self._pt_model.replyBtn = None
									workbook.close()
								elif response == QMessageBox.Ignore:
									self._pt_model.update_template_status(usage_type, 'i')
									self._pt_model.replyBtn = None
									success = True
								elif response == QMessageBox.Close:
									self._abort_flg = True
									self._pt_model.replyBtn = None
									success = True

					if self._cancel_flg:break;

					#Save to workbook in output folder

					status = self._pt_model.get_template_status(usage_type)

					if status == '' and not self._abort_flg: 

						success = False
						while not success:
							try:
								self.txtProgress.emit('Started: Processing {} - Saving Workbook to Output Folder.'.format(usage_type))

								writer.save()

								self.txtProgress.emit('Finished: Processing {} - Saving Workbook to Output Folder.'.format(usage_type))
								time.sleep(3)

								#Update Status
								self._pt_model.update_template_status(usage_type,'c')

								success = True
							except Exception as e:

								self.currStatus.emit([usage_type,'Save Template',wb_name,str(e)])

								response = None
								while response is None:
									response = self._pt_model.replyBtn
									time.sleep(1)

									if response == QMessageBox.Abort:
										self._abort_flg = True
										self._pt_model.replyBtn = None
										success = True
									elif response == QMessageBox.Retry:
										self._pt_model.replyBtn = None
									elif response == QMessageBox.Ignore:
										self._pt_model.update_template_status(usage_type, 'i')
										self._pt_model.replyBtn = None
										success = True
									elif response == QMessageBox.Close:
										self._abort_flg = True
										self._pt_model.replyBtn = None
										success = True
					else:

						workbook.close()

				self._progress_count += 1
				self.countProgress.emit(self._progress_count)

		### Display Elapsed Time ###

		self.update_elapsed_time()

		self.txtProgress.emit('Finished')   

	def update_elapsed_time(self):

		secs = self.timer.elapsed() / 1000
		mins = (secs / 60) % 60
		hours = (secs / 3600)
		seconds = secs % 60

		self.elapsed_time = str(hours).split('.')[0] + ' Hours ' + str(mins).split('.')[0] + ' Minutes ' + str(seconds).split('.')[0] + ' Seconds'

