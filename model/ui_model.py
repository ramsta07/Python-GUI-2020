#!/usr/bin/env python

# Filename: ui_model.py

"""This app is for the Amadeus automation tasks."""

from collections import OrderedDict, defaultdict
import os
import json

class main_app_Model:
	def __init__(self):
		self._usageflows = OrderedDict()
		self._open_doc = defaultdict(lambda: 'open ')
		self._open_doc['Windows'] = 'start'

		self._conf_data = self.parse_config('config.json')

	############ USAGE FLOW LIST ##########

	def add_usageflow(self, usageflow):
		self._usageflows[usageflow] = OrderedDict()
	
	def get_usageflows(self):
		return list(self._usageflows.keys()) # Python 3.0+ conversion

	def remove_usageflow(self, usage_type):
		copyOfDict = dict(self._usageflows)
		for key, items in copyOfDict.items():
			if key == usage_type:
				self.add_usageflow(key)

	############ ADD USAGE TYPE ############
	
	def get_usage_types(self):
		return [key for key, items in self._usageflows.items() if items]

	def get_usage_type_details(self, usage_flow, usage_type):
		return self._usageflows[usage_flow][usage_type]

	def check_dup_usage_type(self, usage_type):
		
		for key, items in self._usageflows.items():
			if items:
				for i in items:
					if i == usage_type:
						return True
					else:
						continue
					return False

	def delete_usage_types(self):

		for key, items in self._usageflows.items():
			if items:
				del self._usageflows[key][key]

			
	def add_usagetype(self, usage_type):

		#Get Usage type name and report name
		usage_name, report_name = self.search_usagetype(usage_type)

		self._usageflows[usage_type][usage_type] = [usage_name, report_name] 
		

	def search_usagetype(self, usage_type):

		for u in self._conf_data['usageFlows']:
			if u['UsageType'] == usage_type:
				return (u['UsageName'],u['ReportName'])

	def get_usagetype_by_report_type(self, selection):

		l_usagetype = []

		for u in self._conf_data['usageFlows']:
			if u['ReportType'] == selection:
				l_usagetype.append(u['UsageType'])

		return l_usagetype

	############ CONFIG ################

	def parse_config(self, json_file):

		#read config file

		curr_dir = os.getcwd()

		with open(curr_dir + '\\resources\\reference\\' + json_file, 'r') as conf:
			data = conf.read()

		#parse file 

			obj = json.loads(data)

		return obj