#!/usr/bin/env python3

# Filename: contract_template_main.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os
import pandas as pd
import xlsxwriter

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QMessageBox

class Contract_Template_Main(QThread):

	"""
	Runs in thread.
	"""

	currStatus = pyqtSignal(list)
	txtProgress = pyqtSignal(str)
	countProgress = pyqtSignal(int)
	isCancel = pyqtSignal(bool)

	def __init__(self, ct_file, src_file, tgt_folder, keyword, ct_model, com_model):
		super(Contract_Template_Main, self).__init__()

		self._ct_file = ct_file
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
		self.txtProgress.emit('Initializing Contract Type Template.')
		time.sleep(3)

		self.temp_workbook = self._ct_model.load_workbook(self._ct_file)
		temp_sheet = self.temp_workbook.sheets[0]

		ws_name = temp_sheet.name.lower()

		if ws_name == 'template':

			success = False
			while not success:
				try:

					if self._cancel_flg: break; self.cancel_program()
					self.txtProgress.emit('Started : Loading source file to dataframe.')
					time.sleep(3)

					ct_df = self._ct_model.readSourceFiletoDF(self._src_file, self._ct_model._ct_config['Delimeter'])
					success = True

					self.txtProgress.emit('Finished : Loading source file to dataframe.')
					time.sleep(3)
					self._progress_count += 1
					self.countProgress.emit(self._progress_count)


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

							wb_name = 'OTC_TST_Contracts_Type_Template_{}.xlsx'.format(self._keyword.upper())
							self.output_filenm = self._tgt_folder + "\\" + wb_name

							if self._cancel_flg: self.cancel_program(); break;break;
							self.txtProgress.emit('Started : Writing dataframe to Contract Type Template.')
							time.sleep(3)

							df_cnt = self._ct_model.write_DF_to_Excel(ct_df, temp_sheet)

							self.txtProgress.emit('Finished : Writing dataframe to Contract Type Template.')
							time.sleep(3)
							self._progress_count += 1
							self.countProgress.emit(self._progress_count)

							if self._cancel_flg: self.cancel_program(); break;break;
							self.txtProgress.emit('Started : Formatting Contract Type Template.')
							time.sleep(3)

							self._ct_model.format_range(temp_sheet, df_cnt, 4, 2, 1, 'Center')

							self.txtProgress.emit('Finished : Formatting Contract Type Template.')
							time.sleep(3)
							self._progress_count += 1
							self.countProgress.emit(self._progress_count)

							success = True

						except Exception as e:

							self.currStatus.emit([ws_name,'Populate Worksheet',str(e)])

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

							if self._cancel_flg: self.cancel_program(); break;break;
							self.txtProgress.emit('Started : Saving Contract Type Template.')
							time.sleep(3)

							self.temp_workbook.save(self.output_filenm)
							self.temp_workbook.close()

							self._progress_count += 1
							self.countProgress.emit(self._progress_count)
							self.txtProgress.emit('Finished : Saving Contract Type Template.')
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
								break;
							elif response == QMessageBox.Retry:
								self._ct_model.replyBtn = None
							elif response == QMessageBox.Close:
								self._cancel_flg = True
								self._ct_model.replyBtn = None
								break;
								break;

					#Set successful flag
					self.is_successful = True
					

				else:

					self._ct_model.showDialog('warning', 'Contract Type Template', 'Empty Source File Name\n{}.'.format(self._src_file), None, None) 

		else:

			self._ct_model.showDialog('warning', 'Contract Type Template', 'Invalid Template Format\n{}.'.format(self._ct_file), None, None) 


	def cancel_program(self):

		self.txtProgress.emit('Cancelling program...')
		time.sleep(3)

		self.isCancel.emit(self._cancel_flg)