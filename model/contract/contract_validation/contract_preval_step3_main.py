#!/usr/bin/env python3

# Filename: contract_preval_step3_main.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os
import pandas as pd
import xlsxwriter

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QMessageBox

class Contract_Preval_Step3_Main(QThread):

	"""
	Runs in thread.
	"""

	currStatus = pyqtSignal(list)
	txtProgress = pyqtSignal(str)
	countProgress = pyqtSignal(int)
	isCancel = pyqtSignal(bool)

	def __init__(self, keyword, temp_file, tgt_folder, l_details, ct_model, com_model):
		super(Contract_Preval_Step3_Main, self).__init__()

		self._keyword = keyword
		self._temp_file = temp_file
		self._tgt_folder = tgt_folder
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


		self._progress_count += 1
		self.countProgress.emit(self._progress_count)
		self.txtProgress.emit('Initializing Contract PreVal Step 3 Template.')
		time.sleep(3)

		self.temp_workbook = self._ct_model.load_workbook(self._temp_file)


		for worksheet,src_file in self._l_details:
			
			if not self._abort_flg :

				success = False
				while not success:
					try:
						
						temp_sheet = self.temp_workbook.sheets[worksheet]

						if self._cancel_flg: self.cancel_program(); break;break;
						self.txtProgress.emit('Started : Loading source file for {} to dataframe.'.format(worksheet))
						time.sleep(3)
						self._progress_count += 1
						self.countProgress.emit(self._progress_count)

						temp_df = self._ct_model.readSourceFiletoDF(src_file, self._ct_model._cv3_config['Delimeter'])
						success = True

						self.txtProgress.emit('Finished : Loading source file for {} to dataframe.'.format(worksheet))
						time.sleep(3)
						self._progress_count += 1
						self.countProgress.emit(self._progress_count)

						if self._cancel_flg: self.cancel_program(); break;break;
						self.txtProgress.emit('Started : Writing dataframe to {}.'.format(worksheet))
						time.sleep(3)

						df_cnt = self._ct_model.write_DF_to_Excel(temp_df, temp_sheet ,'A3')

						self.txtProgress.emit('Finished : Writing dataframe to {}.'.format(worksheet))
						time.sleep(3)
						self._progress_count += 1
						self.countProgress.emit(self._progress_count)

						if self._cancel_flg: self.cancel_program(); break;break;
						self.txtProgress.emit('Started : Formatting {}.'.format(worksheet))
						time.sleep(3)

						self._ct_model.format_range(temp_sheet, df_cnt, 3, 2, 1, 'Center')

						self.txtProgress.emit('Finished : Formatting {}.'.format(worksheet))
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
							break;
						elif response == QMessageBox.Retry:
							self._ct_model.replyBtn = None
						elif response == QMessageBox.Close:
							self._abort_flg = True
							self._ct_model.replyBtn = None
							break;
			else: break;

		if not self._abort_flg:

			success = False
			while not success:
				try:

					wb_name = 'OTC_TST_Contracts_Step3_After_Transformation_Report_{}.xlsx'.format(self._keyword.upper())
					self.output_filenm = self._tgt_folder + "\\" + wb_name

					if self._cancel_flg: self.cancel_program(); break;
					self.txtProgress.emit('Started : Saving Contract Preval Step 3 Template.')
					time.sleep(3)

					self.temp_workbook.save(self.output_filenm)
					self.temp_workbook.close()

					self.txtProgress.emit('Finished : Saving Contract Preval Step 3 Template.')
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
	

	def cancel_program(self):

		self.txtProgress.emit('Cancelling program...')
		time.sleep(3)

		self.isCancel.emit(self._cancel_flg)