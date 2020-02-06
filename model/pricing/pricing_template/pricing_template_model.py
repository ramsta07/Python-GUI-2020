#!/usr/bin/env python

# Filename: pricing_template_model.py

"""This app is for the Amadeus automation tasks."""

import os
import pandas as pd
import re

from PyQt5.QtWidgets import QDialog, QMessageBox

#Views
from views.pricing.pricing_template.pricing_template_dia import Pricing_Template_Dialog
from views.pricing.pricing_template.template_warning_dia import Template_Warning_Dialog
from views.pricing.pricing_template.pricing_template_report import Pricing_Template_Report
from views.pricing.pricing_template.pricing_template_finish import PricingTemplate_finish
from views.pricing.pricing_template.pricing_template_select import Pricing_Template_Select

import xlwings as xw

# Make not excel file not visible
#xw.App().visible = False

from xlwings.constants import AutoFillType

from collections import OrderedDict, defaultdict
from model.ui_model import main_app_Model
from common.common_model import Common_Model
from common.pandas_model import PandasModel

class Pricing_Template_Model():

	def __init__(self, QMainWindow):

		self.ParentWindow = QMainWindow
		self._templates = OrderedDict()
		self._open_doc = defaultdict(lambda: 'open ')
		self._open_doc['Windows'] = 'start'

		self._model_ui = main_app_Model()
		self._common_mod = Common_Model()

		# Initialize Dialogs

		self.Dialog = QDialog(self.ParentWindow)
		self.dialog_ui = Pricing_Template_Dialog()
		self.dialog_ui.setupUi(self.Dialog)

		self.Dialog_warn = QDialog(self.ParentWindow)
		self.dialog_warn_ui = Template_Warning_Dialog()
		self.dialog_warn_ui.setupUi(self.Dialog_warn)

		self.Dialog_finish = QDialog(self.ParentWindow)
		self.Dialog_fin_ui = PricingTemplate_finish()
		self.Dialog_fin_ui.setupUi(self.Dialog_finish)

		self.Dialog_report = QDialog(self.ParentWindow)
		self.Dialog_report_ui = Pricing_Template_Report()
		self.Dialog_report_ui.setupUi(self.Dialog_report)

		self.Dialog_select = QDialog(self.ParentWindow)
		self.Dialog_select_ui = Pricing_Template_Select()
		self.Dialog_select_ui.setupUi(self.Dialog_select)

		self._config = self._model_ui._conf_data['PricingTempConfig']
		self._usageflow_conf = self._model_ui._conf_data['usageFlows']
		
		self.replyBtn = None

	##################### TEMPLATE UI #####################

	def add_templates(self, usage_type):
		self._templates[usage_type] = OrderedDict()

	def check_pricing_templates(self, l_usage_type):

		folder_path = os.getcwd() + "\\resources\\" + self._config['TemplateFolder']

		for usage_type in l_usage_type:

			self.add_templates(usage_type)

			#Check pricing template 

			for r, d, f in os.walk(folder_path):
				for file in f:

					for usage_flow in self._usageflow_conf:
						if usage_flow['UsageType'] == usage_type:
							report_name = usage_flow['ReportName']
							break

					if report_name.lower() in file.lower():
						
						self._templates[usage_type] = [os.path.join(r, file),'']
						break

					else:
						self._templates[usage_type] = [None]

	def get_template_filename(self, usage_type):
		return self._templates[usage_type][0]

	def get_template_status(self, usage_type):
		return self._templates[usage_type][1]

	def update_template_status(self, usage_type, status):
		self._templates[usage_type][1] = status

	def get_template_list(self, l_usage_type):
		self.check_pricing_templates(l_usage_type)
		return [t for t in list(self._templates.items()) if t[1][0]]

	def get_template_list_not_found(self, l_usage_type):
		self.check_pricing_templates(l_usage_type)
		return [t for t in list(self._templates.items()) if not t[1][0]]

	def remove_template_list(self):

		# Create a temporary copy of dictionary

		copyOfDict = dict(self._templates)
		
		for key, items in copyOfDict.items():
			del self._templates[key]

	def get_template_counts(self):

		cnt_source = {}

		for usage_type, logs in self._templates.items():

			l_counts = []

			if logs[0] != None:

				d_counts = logs[3]
				
				if d_counts:
					for val in d_counts.values():

						if isinstance(val, dict):
							l_counts.append(val['Template'])

				if len(l_counts) != 0:
					cnt_source[usage_type] = l_counts
				else:
					cnt_source[usage_type] = [0 ,0 ,0]

		return cnt_source

	def get_missing_columns_df(self):

		l_columns = []
		l_headers = ['Usage Type', 'Report Name', 'Sheet Name', 'Column Name']
		
		for usage_type, logs in self._templates.items():

			if logs[0] != None:

				d_mappings = logs[2]

				if d_mappings:

					reportName = self.get_template_filename(usage_type).split("\\")[-1]

					for key, value in d_mappings.items():

						for col in value:

							sheetName = col['Sheet']
							columnName = col['Template_Column']

							if columnName != 'Billing material description' and columnName != 'As IS BM ID':
								tupRow = (usage_type, reportName, sheetName, columnName)
								l_columns.append(tupRow)

		df = pd.DataFrame().from_records(l_columns, columns=l_headers)
		model = PandasModel(df)

		return model

	def append_template_logs(self, usage_type, step_cnt, key, data):

		if len(self._templates[usage_type]) == step_cnt:
			
				try:
					self._templates[usage_type].append({key: data})
				except IndexError:
					pass
		else:

			self._templates[usage_type][step_cnt][key] = data


	#################### MAIN PROGRAM ##########################

	def filter_df(self, usage_type, df_all):

		filter_DF = df_all[df_all['USAGE_TYPE_CD'] == usage_type]

		#Fill Nan as ''

		filter_DF.fillna(value='',inplace=True)

		return filter_DF

	def read_source_to_DF(self, keyword, folder, pricing_tab):

		pd.options.mode.chained_assignment = None

		config = self._model_ui._conf_data[pricing_tab+'Config']

		src_filename = folder + "\\" +  config[pricing_tab+'FName'] + keyword + '.txt'
		sep = config[pricing_tab+'Delm'] 
		
		df = pd.read_csv(src_filename, sep, engine='python', encoding='utf-8', na_filter = False)

		return df

	def load_workbook(self, template):

		workbook = xw.Book(template)
		xw.App().visible = False
		return workbook

	def get_worksheets(self, workbook):
		
		worksheets = workbook.sheets
		return worksheets

	def get_template_mappings(self, usage_type, sheet, df, pricing_tab):

		'''
		Loop through the columns and get the field to field mapping
		from template to source.
		'''

		#Initialize lists

		template_columns = []
		l_mapping = []
		l_nomapping = []
		d_mapping = {}

		#Get Template Header Information

		start_col = sheet.range('A2').get_address(False, False)
		last_col = sheet.range('A2').end('right').get_address(False, False)
		col_range = sheet.range(start_col, last_col)

		for c in col_range:
			template_columns.append((c.value, c.address.replace('$','')))
		
		#Get Source Columns

		src_columns = list(df.columns) 

		# Get column mappings
		
		for col in template_columns:

			temp_column = col[0]
			temp_cell = col[1]

			if temp_column.lower() in [' '.join(col.lower().split('_')[1:]) for col in src_columns]:

				for src_col in src_columns:

					column_drv = ' '.join(src_col.lower().split('_')[1:])

					if temp_column.lower() == column_drv:

						d_mapping = {'Usage_Type': usage_type, 'Sheet': sheet.name, 'Source_Column': src_col, 'Template_Column': temp_column, 'Template_Cell' : temp_cell}

			else:

				l_nomapping.append({'Sheet': sheet.name, 'Template_Column': temp_column, 'Template_Cell' : temp_cell})

			if d_mapping: l_mapping.append(d_mapping)

		# Update templates OD 

		key_tab = pricing_tab + '-' + sheet.name

		self.append_template_logs(usage_type, 2, key_tab, l_nomapping)

		return l_mapping


	def merge_scale_price_df(self, df_scales, df_price):

		merged_df = pd.merge(df_scales,df_price,how='inner',left_on=['Short_Text_Key','PARTNER_NUMBER','PRODUCT_ID','BILLING_MATERIAL_ID','SCALE_ID_MAP'], right_on = ['Short_Text_Key','fld_Business_Partner','HybrisProduct_ID','fld_OTC_Billing_Material_ID','fld_Scale_ID'])

		return merged_df

	def merge_minf_price_df(self, df_minf, df_price):

		merged_df = pd.merge(df_minf,df_price,how='inner',left_on=['Short_Text_Key','Partner_Number','Product_ID','Billing_Material_ID','Counter_ID'], right_on = ['Short_Text_Key','fld_Business_Partner','HybrisProduct_ID','fld_OTC_Billing_Material_ID','fld_MF_Counter'])

		return merged_df

	def delete_rows(self, sheet, start_row):

		min_range = 'A'+str(start_row)

		#Get Max range

		max_rows = (sheet.api.UsedRange.Row,sheet.api.UsedRange.Row + sheet.api.UsedRange.Rows.Count)[-1]
		last_col = sheet.range('A2').end('right').get_address(False, False)
		max_range = re.sub('[0-9]', '', last_col) + str(max_rows)

		sheet.range(min_range+':'+max_range).clear()

	def prepare_worksheet(self, sheet, start_row, max_row):

		# Initialize formatting styles

		if max_row == 0:

			self.delete_rows(sheet, start_row)

		else:

			start_range = 'A'+str(start_row)

			#Delete rows
			self.delete_rows(sheet, start_row+1)

			#Autofill

			last_row = (start_row - 1) + max_row
			
			if max_row != 1:
				sheet.range('$'+str(start_row)+':$'+str(start_row)).api.AutoFill(sheet.range('$'+str(start_row)+':$'+str(last_row)).api,AutoFillType.xlFillDefault)

	def format_worksheet(self, sheet, start_row):

		low_range = 'A' + str(start_row)
		high_range = get_column_letter(sheet.max_column)+str(sheet.max_row)

		self.set_border_range(sheet, low_range+":"+high_range,'thin')

	def set_border_range(self, ws, cell_range, border_type):

		thin_border = Border(left=Side(style=border_type), 
							right=Side(style=border_type), 
							top=Side(style=border_type), 
							bottom=Side(style=border_type))

		for row in ws[cell_range]:
			for cell in row:
				cell.border = thin_border

	def populate_worksheet(self, sheet, df, l_mapping, start_row):
		
		for d in l_mapping:

			startingrow = start_row

			temp_column_cell = re.sub('[^a-zA-Z]+', '', d['Template_Cell'])
			src_column = d['Source_Column']
			
			#Get source values for each columns

			if 'date' in src_column.lower():
				l_values = ['\''+ str(x) for x in df[src_column].values.tolist()]
			else:
				l_values = df[src_column].values.tolist()

			sheet.range(temp_column_cell + str(startingrow)).options(transpose=True).value = l_values

		row_cnt = len(l_values)

		return row_cnt

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
			msg.setStandardButtons(QMessageBox.Abort | QMessageBox.Retry | QMessageBox.Ignore | QMessageBox.Close)
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