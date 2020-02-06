#!/usr/bin/env python3

# Filename: debit_credit_main.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os
import pandas as pd
import xlsxwriter

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QMessageBox

class Debit_Credit_Main(QThread):

	"""
	Runs in thread.
	"""

	currStatus = pyqtSignal(list)
	txtProgress = pyqtSignal(str)
	countProgress = pyqtSignal(int)
	isCancel = pyqtSignal(bool)

	def __init__(self, keyword, tgt_folder, l_template, l_details, ct_model, com_model):
		super(Debit_Credit_Main, self).__init__()

		self._keyword = keyword
		self._tgt_folder = tgt_folder
		self._l_template = l_template
		self._l_details = l_details
		self._ct_model = ct_model
		self._common_mod =com_model
		
		self.timer = QTime()
		self.elapsed_time = None
		self._progress_count = 0

		self.is_running = True
		self.is_successful = False
		self._abort_flg = False
		self._cancel_flg = False
		self._main_dir = os.getcwd()

	def run(self):

		''' 
		Read source file to DataFrame 
		Populate Contract Type Template
		'''

		# Start timer
		
		self.timer.start()

		self.txtProgress.emit('Initializing Debit Credit Enrichment Template.')
		time.sleep(3)


		for template,file in self._l_template:

			self._progress_count += 1
			self.countProgress.emit(self._progress_count)
			self.txtProgress.emit('Initializing {} Enrichment Template.'.format(template))
			time.sleep(3)

			self.temp_workbook = self._ct_model.load_workbook(file)

			for template_details,worksheet,src_file in self._l_details:
				
				if template == template_details and not self._abort_flg:

					success = False
					while not success:
						try:
							
							temp_sheet = self.temp_workbook.sheets[worksheet]

							if self._cancel_flg: self.cancel_program(); break;break;break;
							self.txtProgress.emit('Started : {} - Loading source file for {} to dataframe.'.format(template, worksheet))
							time.sleep(3)
							self._progress_count += 1
							self.countProgress.emit(self._progress_count)

							temp_df = self._ct_model.readSourceFiletoDF(src_file, self._ct_model._ct_config['Delimeter'])
							
							self.txtProgress.emit('Finished : {} - Loading source file for {} to dataframe.'.format(template, worksheet))
							time.sleep(3)
							self._progress_count += 1
							self.countProgress.emit(self._progress_count)

							if self._cancel_flg: self.cancel_program(); break;break;break;
							self.txtProgress.emit('Started : {} - Writing dataframe to {}.'.format(template,worksheet))
							time.sleep(3)

							df_cnt = self._ct_model.write_DF_to_Excel(temp_df, temp_sheet)

							self.txtProgress.emit('Finished : {} - Writing dataframe to {}.'.format(template,worksheet))
							time.sleep(3)
							self._progress_count += 1
							self.countProgress.emit(self._progress_count)

							if self._cancel_flg: self.cancel_program(); break;break;break;
							self.txtProgress.emit('Started : {} - Formatting {}.'.format(template,worksheet))
							time.sleep(3)

							self._ct_model.format_range(temp_sheet, df_cnt, 4, 2, 1, 'Center')

							self.txtProgress.emit('Finished : {} - Formatting {}.'.format(template,worksheet))
							time.sleep(3)
							self._progress_count += 1
							self.countProgress.emit(self._progress_count)

							success = True

						except Exception as e:

							self.currStatus.emit([temp_sheet.name,'Populate Worksheet',str(e)])

							response = None
							while response is None:
								response = self._ct_model.replyBtn
								time.sleep(1)

							if response == QMessageBox.Abort:
								self._abort_flg = True
								self._ct_model.replyBtn = None
								success=True
								break;
							elif response == QMessageBox.Retry:
								self._ct_model.replyBtn = None
							elif response == QMessageBox.Close:
								self._abort_flg = True
								self._ct_model.replyBtn = None
								success = True
								break;
				else:

					break;

			if not self._abort_flg:

				success = False
				while not success:
					try:

						wb_name = 'OTC_TST_{}_Enrichment_Template_{}.xlsx'.format(template,self._keyword.upper())
						self.output_filenm = self._tgt_folder + "\\" + wb_name

						if self._cancel_flg: self.cancel_program(); break;break;
						self.txtProgress.emit('Started : Saving {} Enrichment Template.'.format(template))
						time.sleep(3)

						self.temp_workbook.save(self.output_filenm)
						self.temp_workbook.close()

						self.txtProgress.emit('Finished : Saving {} Enrichment Template.'.format(template))
						time.sleep(3)

						success = True

					except Exception as e:

						self.currStatus.emit([self.output_filenm,'Save Template',str(e)])

						response = None
						while response is None:
							response = self._ct_model.replyBtn
							time.sleep(1)
						if response == QMessageBox.Abort:
							self._cancel_flg = True
							self._ct_model.replyBtn = None
							break;
						elif response == QMessageBox.Retry:
							self._ct_model.replyBtn = None
						elif response == QMessageBox.Close:
							self._cancel_flg = True
							self._ct_model.replyBtn = None
							break;

				#Set successful flag

				self.is_successful = True
			
			else:

				break;


	def cancel_program(self):

		self.txtProgress.emit('Cancelling program...')
		time.sleep(3)

		self.isCancel.emit(self._cancel_flg)