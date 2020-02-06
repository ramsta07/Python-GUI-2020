#!/usr/bin/env python3

# Filename: contract_preval_step1_main.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os
import pandas as pd
import xlsxwriter

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QMessageBox

class Contract_Preval_Step1_Main(QThread):

	"""
	Runs in thread.
	"""

	currStatus = pyqtSignal(list)
	txtProgress = pyqtSignal(str)
	countProgress = pyqtSignal(int)
	isCancel = pyqtSignal(bool)

	def __init__(self, temp_file, src_file, tgt_folder, keyword, ct_model, com_model):
		super(Contract_Preval_Step1_Main, self).__init__()

		self._temp_file = temp_file
		self._src_file = src_file
		self._tgt_folder = tgt_folder
		self._keyword = keyword
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

		self._progress_count += 1
		self.countProgress.emit(self._progress_count)
		self.txtProgress.emit('Initializing Contract PreVal Step 1 Template.')
		time.sleep(3)

		self.temp_workbook = self._ct_model.load_workbook(self._temp_file)
		temp_ws = self._ct_model._cv1_config['PrevalStep1SheetName']
		temp_sheet = self.temp_workbook.sheets[temp_ws]

		success = False
		while not success:
			try:

				if self._cancel_flg: break; self.cancel_program()
				self.txtProgress.emit('Started : Loading source file to dataframe.')
				time.sleep(3)

				ct_df = self._ct_model.readSourceFiletoDF(self._src_file, self._ct_model._cv1_config['Delimeter'])

				self.txtProgress.emit('Finished : Loading source file to dataframe.')
				time.sleep(3)
				self._progress_count += 1
				self.countProgress.emit(self._progress_count)

				success=True

			except Exception as e:

				self.currStatus.emit([self._keyword,'Load Source',str(e)])

				response = None
				while response is None:
					response = self._ct_model.replyBtn
					time.sleep(1)

				if response == QMessageBox.Close:
					self._abort_flg = True
					self._ct_model.replyBtn = None
					success = True

		if not self._abort_flg:

			if not ct_df.empty:

				# Write to Excel

				success = False
				while not success:
					try:

						wb_name = 'OTC_TST_Contracts_Step1_AS-IS_Extract_Validation_Report_{}.xlsx'.format(self._keyword.upper())
						self.output_filenm = self._tgt_folder + "\\" + wb_name

						if self._cancel_flg: self.cancel_program(); break;
						self.txtProgress.emit('Started : Writing dataframe to Contract Preval Step1 Template.')
						time.sleep(3)

						df_cnt = self._ct_model.write_DF_to_Excel(ct_df, temp_sheet, 'A2')

						self.txtProgress.emit('Finished : Writing dataframe to Contract Preval Step1 Template.')
						time.sleep(3)
						self._progress_count += 1
						self.countProgress.emit(self._progress_count)

						if self._cancel_flg: self.cancel_program(); break;
						self.txtProgress.emit('Started : FormattingContract Preval Step1 Template.')
						time.sleep(3)

						self._ct_model.format_range(temp_sheet, df_cnt, 2, 2, 1,'Center')

						self.txtProgress.emit('Finished : Formatting Contract Preval Step1 Template.')
						time.sleep(3)
						self._progress_count += 1
						self.countProgress.emit(self._progress_count)

						success = True

					except Exception as e:

						self.currStatus.emit([temp_ws,'Populate Worksheet',str(e)])

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

				success = False
				while not success:
					try:

						if self._cancel_flg: self.cancel_program(); break;
						self.txtProgress.emit('Started : Saving Contract Preval Step 1 Template.')
						time.sleep(3)

						self.temp_workbook.save(self.output_filenm)
						self.temp_workbook.close()

						self._progress_count += 1
						self.countProgress.emit(self._progress_count)
						self.txtProgress.emit('Finished : Saving Contract Preval Step 1 Template.')
						time.sleep(3)

						#Set successful flag

						self.is_successful = True

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

				self._ct_model.showDialog('warning', 'Contract Preval Step1 Template', 'Empty Source File Name\n{}.'.format(self._src_file), None, None) 


	def cancel_program(self):

		self.txtProgress.emit('Cancelling program...')
		time.sleep(3)
			
		self.isCancel.emit(self._cancel_flg)