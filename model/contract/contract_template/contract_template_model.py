#!/usr/bin/env python

# Filename: contract_template_model.py

"""This app is for the Amadeus automation tasks."""

import os
import pandas as pd
import re
import xlwings as xw
from xlwings import constants 

from PyQt5.QtWidgets import QDialog, QMessageBox

#Views
from views.contract.contract_template.contract_template_dia import Contract_Template_Dialog

#Models
from model.ui_model import main_app_Model
from common.common_model import Common_Model

class Contract_Template_Model():

	def __init__(self, QMainWindow):

		self.ParentWindow = QMainWindow

		self._model_ui = main_app_Model()
		self._common_mod = Common_Model()

		# Initialize Dialogs

		self.Dialog = QDialog(self.ParentWindow)
		self.dialog_ui = Contract_Template_Dialog()
		self.dialog_ui.setupUi(self.Dialog)

		self._ct_config = self._model_ui._conf_data['ContractTempConfig']
		self._dc_config = self._model_ui._conf_data['DebitCreditConfig']
		self._cv1_config = self._model_ui._conf_data['ContractPreValStep1Config']
		self._cv3_config = self._model_ui._conf_data['ContractPreValStep3Config']

		self.replyBtn = None

	def checkContractTypeTemplate(self, folder_path, template_name):

		#Check pricing template 

		for r, d, f in os.walk(folder_path):
			for file in f:

				if template_name.lower() in file.lower():	
					exist = True
					break
				else:
					exist = False

		return exist

	def checkDebitCreditTemplate(self, folder_path, selected):

		l_missing = []
		l_template = []

		if selected == "All":

			template_name = self._dc_config['TemplateFName']
			
			for i in ['Debit', 'Credit']:
				
				template_fname = i + template_name + '.xlsx'
				template_filepath = folder_path +'\\'+ template_fname

				for r, d, f in os.walk(folder_path):
					for file in f:

						if template_fname.lower() in file.lower():	
							exist=True
							break
						else:
							exist=False

				l_template.append((i,template_filepath))
				if not exist: l_missing.append((i,template_fname))
		else:

			template_name = self._dc_config['TemplateFName']
			template_fname = selected + template_name + '.xlsx'
			template_filepath = folder_path +'\\'+ template_fname

			for r, d, f in os.walk(folder_path):
				for file in f:

					if template_fname.lower() in file.lower():	
						exist = True
						break
					else:
						exist = False
			
			l_template.append((selected,template_filepath))
			if not exist: l_missing.append((selected,template_fname))

		return (l_template,l_missing)

	def checkDebitCreditSource(self, keyword, source_path, selected):

		l_missing = []
		l_details = []

		if selected == "All":
				
			for i in ['Debit', 'Credit']:
				
				l_sheets = self._dc_config[i]

				for s in l_sheets:

					exist=False
					sheet = s['SheetName']
					src_filenm = '{}{}.csv'.format(s['SourceFName'],keyword)
					src_filepath = source_path +'\\'+ src_filenm

					for r, d, f in os.walk(source_path):
						for file in f:

							if src_filenm.lower() in file.lower():	
								exist=True
								break	
					
					l_details.append((i,sheet,src_filepath))
					if not exist: l_missing.append((i,sheet,src_filepath))
		else:

			l_sheets = self._dc_config[selected]

			for s in l_sheets:

				exist=False
				sheet = s['SheetName']
				src_filenm = '{}{}.csv'.format(s['SourceFName'],keyword)
				src_filepath = source_path +'\\'+ src_filenm

				for r, d, f in os.walk(source_path):
					for file in f:

						if src_filenm.lower() in file.lower():	
							exist=True
							break			
				
				l_details.append((selected,sheet,src_filepath))
				if not exist: l_missing.append((selected,sheet,src_filenm))

		
		return (l_details, l_missing)

	def checkContractPreValStep3Source(self, keyword, source_path):

		l_missing = []
		l_details = []

		l_sheets = self._cv3_config['Sheets']

		for s in l_sheets:

			exist=False
			sheet = s['SheetName']
			src_filenm = '{}_{}.csv'.format(s['SourceFName'],keyword)
			src_filepath = source_path +'\\'+ src_filenm

			for r, d, f in os.walk(source_path):
				for file in f:

					if src_filenm.lower() in file.lower():	
						exist=True
						break			
			
			l_details.append((sheet,src_filepath))
			if not exist: l_missing.append((sheet,src_filenm))

		
		return (l_details, l_missing)

	def readSourceFiletoDF(self, src_file, delimeter):

		pd.options.mode.chained_assignment = None
		sep = delimeter

		df = pd.read_csv(src_file, sep, engine='python',
						converters={
						"AS_IS_Document": str,
						"ASIS_Document": str,
						"AS_IS_Document_Item": str,
						"ASIS_Document_Item": str,
						"Billing_Material_ASIS": str, # Ensure fields is read as string, maintaining leading 0's
						"Billing_Material_AsIs_ID": str,
						"Master_Agreement_GUID": str,
						"Master_Agreement_Partner":str,
						"Authorized_Partner":str,
						"Sold_To_Party":str,
						"BP_Bill_To": str,
						"Customer_Contact": str,
						"Revenue_Contact": str,
						"Collections_Contact": str,
						"Extended_Account_Manager": str,
						"Account_Manager": str,
						"Legal_Department": str,
						"Payer": str,

						### Validations ###

						"Tmp_AS_IS_Document": str,
						"ASIS_CONTRACT": str,
						"Tmp_AS_IS_Document_Item":str,
						"ASIS_CONTRACT_ITEM":str,
						"Tmp_Billing_Material_ASIS":str,
						"MATERIAL":str,
						},
						#dtype=str,
						encoding='utf-8',
						na_filter = False)

		return df

	def load_workbook(self, template):

		workbook = xw.Book(template)
		xw.App().visible = False
		return workbook

	def format_range(self, sheet, df_cnt, start_cell, border_weight, border_style, align):

		#Get Template Header Information

		cell_col = sheet.range('A1').end('right').get_address(False, False)
		
		
		if len(cell_col) > 2:
			last_col = cell_col[:2]
		else:
			last_col = cell_col[0]

		min_cell = int(start_cell) - 1
		xl_range = 'A{}:'.format(start_cell) + last_col + str((df_cnt+min_cell))
		fil_range = 'A{}:'.format(str(min_cell)) + last_col + str(min_cell)

		print(xl_range)
		### set up border weight
		if border_weight > 0:
			sheet.range(xl_range).api.Borders(1).Weight = border_weight ### sets vertical 
			sheet.range(xl_range).api.Borders(2).Weight = border_weight ### sets vertical 
			sheet.range(xl_range).api.Borders(3).Weight = border_weight ### sets horizontal top needs to be one row more 
			sheet.range(xl_range).api.Borders(4).Weight = border_weight ### sets nottom

		### set up border style
		if border_style > 0:
			sheet.range(xl_range).api.Borders(1).LineStyle = border_style
			sheet.range(xl_range).api.Borders(1).LineStyle = border_style
			sheet.range(xl_range).api.Borders(1).LineStyle = border_style

		### add auto filter

		sheet.range(fil_range).api.AutoFilter(1)

		# ### set up alignment
		# if align =='Center':
		# 	xw.Range(xlrange).api.HorizontalAlignment = constants.HAlign.xlHAlignCenter
		# if align =='Right':
		# 	xw.Range(xlrange).api.HorizontalAlignment = constants.HAlign.xlHAlignRight
		# if align =='Left':
		# 	xw.Range(xlrange).api.HorizontalAlignment = constants.HAlign.xlHAlignLeft

	def write_DF_to_Excel(self, df, sheet, startcell='A4', chunk_size=100000):

		df_cnt = int(df.shape[0])

		print(startcell)
		# sheet.range(startcell).options(index=False, header=False).value = df

		if df_cnt <= (chunk_size + 1):
			sheet.range(startcell).options(index=False, header=False).value = df
		else: # Chunk df and and dump each
			c = re.match(r"([a-z]+)([0-9]+)", startcell, re.I) # A1
			row = c.group(1) # A
			col = int(c.group(2)) # 2 - 1

			for chunk in (df[rw:rw + chunk_size] for rw in range(0, df_cnt, chunk_size)):
				print("Dumping chunk in %s%s" %(row, col))
				sheet.range(row + str(col)).options(index=False, header=False).value = chunk
				col += chunk_size

		return df_cnt

	def showDialog(self, msg_type, title, message, addtl_msg, detailed_msg, isCancel=False):

		msg = QMessageBox()

		# Set Icon

		if msg_type.lower() == 'inform': 
			msg.setIcon(QMessageBox.Information)
			msg.setStandardButtons(QMessageBox.Close)
		elif msg_type.lower() == 'warning':
			msg.setIcon(QMessageBox.Warning)
			msg.setStandardButtons(QMessageBox.Close)
		elif msg_type.lower() == 'error':
			msg.setIcon(QMessageBox.Critical)
			msg.setStandardButtons(QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Close)
		else:
			msg.setIcon(QMessageBox.Question)
			msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		msg.setText(message)
		#msg.setInformativeText("This is additional information")
		msg.setWindowTitle(title)
		
		if addtl_msg is not None:
			msg.setInformativeText(addtl_msg)

		if detailed_msg is not None:
			msg.setDetailedText(detailed_msg)

		self.replyBtn = msg.exec_()

		if isCancel:
			return self.replyBtn