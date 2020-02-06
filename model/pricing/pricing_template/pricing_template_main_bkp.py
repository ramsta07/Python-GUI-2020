#!/usr/bin/env python3

# Filename: pricing_template_main.py

"""This app is for the Amadeus automation tasks."""

import sys, time
import os
import pandas as pd
import numpy as np

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTime
from PyQt5.QtWidgets import QMessageBox

class Pricing_Template_Main(QThread):

    """
    Runs in thread.
    """
    
    txtProgress = pyqtSignal(str)
    countProgress = pyqtSignal(int)
    currStatus = pyqtSignal(list)

    def __init__(self, src_folder, tgt_folder, keyword, templates, pt_model):
        super(Pricing_Template_Main, self).__init__()
        
        self._src_folder = src_folder
        self._tgt_folder = tgt_folder
        self._keyword = keyword
        self._l_templates = templates
        self._pt_model = pt_model

        self.timer = QTime()
        self.elapsed_time = None

        self.is_running = True
        self._progress_count = 0
        self._abort_flg = False
        self._cancel_flg = False
        self._main_dir = os.getcwd()

        self.src_price_cnt = 0
        self.temp_price_cnt = 0
        self.src_scales_cnt = 0
        self.temp_scales_cnt = 0
        self.src_minf_cnt = 0
        self.temp_minf_cnt = 0

        self.start_row = self._pt_model._config['StartRow']

    def run(self):
        
        ''' 
        Read source file to DataFrame and Excel file (for validation)
        Filter dataframe per Usage Type
        Perform Mappings
        Populate the validated dataframe to template
        '''

        # Read source files and load to dataframe

        # Start timer

        self.timer.start()

        self.txtProgress.emit('Loading source files to dataframes.')

        success = False
        while not success:
            try:

                self.df_price_all = self._pt_model.read_source_to_DF(self._keyword, self._src_folder, 'Pricing')
                df_scales_all = self._pt_model.read_source_to_DF(self._keyword, self._src_folder,  'Scales')
                df_minf_all = self._pt_model.read_source_to_DF(self._keyword, self._src_folder,  'MINF')

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

                ''' 
                Get current status
                c = Completed
                i = Ignored
                NULL = Not started (default)
                '''

                if self._cancel_flg:break;

                status = self._pt_model.get_template_status(usage_type)

                if status == '':

                    self.txtProgress.emit('Processing '+usage_type)

                    # Get template worksheets

                    template_file = self._pt_model.get_template_filename(usage_type)
                    template_filename = template_file.split('\\')[-1]

                    # Load Template Workbook

                    self.txtProgress.emit('Loading Pricing Template to dataframe.')

                    success = False
                    while not success:
                        try:
                            temp_workbook = self._pt_model.load_workbook(template_file)
                            temp_worksheets = self._pt_model.get_worksheets(temp_workbook)
                            success = True
                        except Exception as e:

                            self.currStatus.emit([usage_type,'Load Template',str(e)])

                            response = None
                            while response is None:
                                response = self._pt_model.replyBtn
                                time.sleep(1)

                            if response == QMessageBox.Abort:
                                self._abort_flg = True
                                self._pt_model.replyBtn = None
                                break;
                            elif response == QMessageBox.Retry:
                                self._pt_model.replyBtn = None
                            elif response == QMessageBox.Ignore:
                                self._pt_model.update_template_status(usage_type, 'i')
                                self._pt_model.replyBtn = None
                                continue;
                            elif response == QMessageBox.Close:
                                self._abort_flg = True
                                self._pt_model.replyBtn = None
                                break;

                    # Filter & Validate Usage type

                    df_price = self._pt_model.filter_df(usage_type, self.df_price_all)
                    df_scales = self._pt_model.filter_df(usage_type, df_scales_all)
                    df_minf = self._pt_model.filter_df(usage_type, df_minf_all)

                    # Prep Source data frame

                    # Drop column fld_Contract_Type

                    df_price.drop('fld_Contract_Type', axis=1, inplace=True)

                    # Rename Column names in dataframe

                    df_price.rename(columns={
                        'Partner_Number': 'fld_Business_Partner',
                        'BillingMaterial_ID_ToBe': 'fld_OTC_Billing_Material_ID',
                        'fld_Requestor': 'fld_Requester', 
                        'fld_Price': 'fld_Price_Amount', 
                        'fld_Pricing_Bundle_ID': 'fld_Bundle_ID',
                        'fld_Pricing_Contract_Type': 'fld_Contract_Type', 
                        'fld_Pricing_Contract_SubType': 'fld_Contract_Sub_Type',
                        'fld_SSCALE_ID': 'fld_Shared_Scale_ID',
                        'fld_SSCALE_BP': 'fld_Shared_Scale_BP',
                        #'fld_Reach_Indicator': 'fld_Reach_Ind',
                        'fld_Flight_Range_Code': 'fld_Flight_Range'}, inplace=True)

                    # Add columns to dataframe
                    # Common Audit Fields

                    df_price['fld_Created_By'] = ''
                    df_price['fld_Last_Upd'] = ''
                    df_price['fld_Last_Upd_By'] = 'DATA MIG'
                    df_price['fld_Created'] = ''

                    self.txtProgress.emit('Processing '+usage_type+ ' - Filtering and Validating dataframe.')

                    #Loop on the template worksheet

                    for sheet in temp_worksheets:
                        
                        success = False
                        while not success:

                            try:

                                if ('price' in sheet.title.lower() and 'scale' not in sheet.title.lower()) or ('minq' in sheet.title.lower() or 'caps' in sheet.title.lower() or 'flight' in sheet.title.lower()): 

                                    self.src_price_cnt = df_price.shape[0]

                                    if not df_price.empty and not self._cancel_flg:

                                        # Mappings for CAP, Flight range and MINQ

                                        if 'minq' in sheet.title.lower() or 'caps' in sheet.title.lower() or 'flight' in sheet.title.lower():

                                            self.txtProgress.emit('Started: Processing '+usage_type+ ' - Additional mappings for ' + sheet.title +'.')

                                            df_price['fld_Counter_ID'] = '*'
                                            df_price['fld_Frequency'] = '*'
                                            df_price['fld_Type_of_Calendar'] = '*'
                                            df_price['fld_Min_Quantity'] = '*'
                                            df_price['fld_Scale_Frequency'] = '*'
                                            df_price['fld_Reference_Date'] = df_price['fld_Start_Date']
                                            df_price['fld_Range'] = '*'
                                            df_price['fld_Scale_Price'] = '*'
                                            df_price['fld_Unit_Price'] = '*'
                                            df_price['fld_CAP'] = '*'
                                            df_price['fld_Billing_Material'] =  df_price['fld_OTC_Billing_Material_ID']

                                            df_price['fld_ID'] = '*'
                                            df_price['fld_Lower_Bound'] = '*'
                                            df_price['fld_Upper_Bound'] = '*'
                                            df_price['fld_Flight_Range_Label'] = '*'

                                            self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Additional mappings for ' + sheet.title +'.')
                                            time.sleep(3)

                                        # Get Mappings

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Getting mappings for ' + sheet.title +'.')

                                        l_mapping = self._pt_model.get_template_mappings(usage_type, sheet, df_price, 'Price')

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Getting mappings for ' + sheet.title +'.')
                                        time.sleep(3)

                                        if 'flight' in sheet.title.lower():
                                            start_row = 3
                                        else:
                                            start_row = self.start_row

                                        # Prepare the worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        #self._pt_model.prepare_worksheet(sheet, start_row, self.src_price_cnt)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Populate data from dataframe to worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Populating worksheet ' + sheet.title +'.')

                                        #self.temp_price_cnt = self._pt_model.populate_worksheet(sheet, df_price, l_mapping, start_row)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Populating worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Format worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Formatting worksheet ' + sheet.title +'.')

                                        #self._pt_model.format_worksheet(sheet, start_row)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Formatting worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                                    
                                    else:

                                        if 'flight' in sheet.title.lower():
                                            start_row = 3
                                        else:
                                            start_row = self.start_row

                                        # Prepare the worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        self._pt_model.prepare_worksheet(sheet, start_row, 0)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                                    
                                        #Insert empty mapping logs

                                        key_tab = 'Price' + '-' + sheet.title

                                        self._pt_model.append_template_logs(usage_type, 2, key_tab, [])

                                        if self._cancel_flg:return;

                                elif 'scale' in sheet.title.lower():

                                    if not df_scales.empty and not self._cancel_flg:

                                        #Merge DataFrame with Price DataFrame

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Merging scales dataframe to Price.')

                                        merged_price_scale_df = self._pt_model.merge_scale_price_df(df_scales, df_price)
                                        
                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Merging scales dataframe to Price.')
                                        time.sleep(3)
                                            
                                        # Mapping logic for Type of calendar and reference_date

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Applying additional scales logic.')

                                        conditions = [
                                                    (merged_price_scale_df['Condition_Type'] == 'ZCUY') | (merged_price_scale_df['Condition_Type'] == 'ZCUA'),
                                                    (merged_price_scale_df['Condition_Type'] == 'ZCUM') | (merged_price_scale_df['Condition_Type'] == 'ZCUX')]

                                        choices = ['Yearly', 'Monthly']
                                        merged_price_scale_df['fld_Scale_Frequency'] = np.select(conditions, choices, default='*')
                        
                                        merged_price_scale_df['fld_Type_of_Calendar'] = merged_price_scale_df[['Condition_Type','fld_Start_Date']].apply(lambda x: 'Natural' if x['Condition_Type'] == 'ZCUM' or x['Condition_Type'] == 'ZCUM' 
                                                                    else ('Natural' if (x['Condition_Type'] == 'ZCUY' or x['Condition_Type'] == 'ZCUA') and x['fld_Start_Date'][:8][4:] == '0101' else 'Rolling'), axis=1)

                                        merged_price_scale_df['fld_Reference_Date'] = merged_price_scale_df[['fld_Type_of_Calendar','fld_Start_Date']].apply(lambda x: x['fld_Start_Date'] if x['fld_Type_of_Calendar'] == 'Rolling' else 'NA', axis=1)

                                        #Add/rename columns to dataframe

                                        merged_price_scale_df['fld_Minimum_Fee'] = '*'
                                        merged_price_scale_df['fld_Minimum_Fee_BM'] = '*'

                                        merged_price_scale_df.rename(columns={
                                            'MAPPING_TABLE': 'fld_Mapping_Table',
                                            'RANGE': 'fld_Range',
                                            'SCALE_PRICE': 'fld_Scale_Price',}, inplace=True)
                                        
                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Applying additional scales logic.')
                                        time.sleep(3)
                                            
                                        # Get Mappings

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Getting mappings for ' + sheet.title +'.')

                                        l_mapping = self._pt_model.get_template_mappings(usage_type, sheet, merged_price_scale_df, 'Scales')

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Getting mappings for ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Prepare the worksheet

                                        self.src_scales_cnt = merged_price_scale_df.shape[0]

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        #self._pt_model.prepare_worksheet(sheet, self.start_row, self.src_scales_cnt)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Populate data from dataframe to worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Populating worksheet ' + sheet.title +'.')

                                        #self.temp_scales_cnt = self._pt_model.populate_worksheet(sheet, merged_price_scale_df, l_mapping, self.start_row)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Populating worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Format worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Formatting worksheet ' + sheet.title +'.')

                                        #self._pt_model.format_worksheet(sheet, self.start_row)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Formatting worksheet ' + sheet.title +'.')
                                        time.sleep(3)

                                    else:

                                        # Prepare the worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        self._pt_model.prepare_worksheet(sheet, self.start_row, 0)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                                    
                                        #Insert empty mapping logs

                                        key_tab = 'Scales' + '-' + sheet.title

                                        self._pt_model.append_template_logs(usage_type, 2, key_tab, [])

                                        if self._cancel_flg:return

                                
                                elif 'minf' in sheet.title.lower():

                                    if not df_minf.empty and not self._cancel_flg:

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing MINQ dataframe ' + sheet.title +'.')

                                        # Drop not needed columns added on price dataframe

                                        df_price.drop(['fld_Counter_ID', 'fld_Frequency', 'fld_Type_of_Calendar', 'fld_Reference_Date', 'fld_Billing_Material'], axis=1, inplace=True)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing MINQ dataframe ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        #Merge DataFrame with Price DataFrame
                                        
                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Merging MINF dataframe to Price.')

                                        df_price_req = df_price[['Short_Text_Key','fld_Business_Partner','HybrisProduct_ID','fld_OTC_Billing_Material_ID','fld_MF_Counter',
                                                                'fld_Discount','fld_Discount_Type','fld_Discount_Description','fld_Item_Category']]
                                    
                                        #Merge DataFrame with Price DataFrame

                                        merged_price_minf_df = self._pt_model.merge_minf_price_df(df_minf, df_price_req)

                                        #Rename columns
                                        merged_price_minf_df.rename(columns={
                                                                'Start_Date':'fld_Reference_Date',
                                                                'Frequency': 'fld_Frequency',
                                                                'Currency':'fld_Currency',
                                                                'fld_OTC_Billing_Material_ID': 'fld_Billing_Material',
                                                                'Minimum_Fee':'fld_Min_Fee',
                                                                'fld_MF_Counter':'fld_Counter_ID',},inplace=True)
                                        
                                        merged_price_minf_df['fld_Type_of_Calendar'] = '*'

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Merging MINF dataframe to Price.')
                                        time.sleep(3)
                                            
                                        # Get Mappings

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Getting mappings for ' + sheet.title +'.')

                                        l_mapping = self._pt_model.get_template_mappings(usage_type, sheet, merged_price_minf_df, 'MINF')

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Getting mappings for ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Prepare the worksheet

                                        self.src_minf_cnt = merged_price_minf_df.shape[0]

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        #self._pt_model.prepare_worksheet(sheet, self.start_row, self.src_minf_cnt)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Populate data from dataframe to worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Populating worksheet ' + sheet.title +'.')

                                        #self.temp_minf_cnt = self._pt_model.populate_worksheet(sheet, merged_price_minf_df, l_mapping, self.start_row)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Populating worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                            
                                        # Format worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        #self._pt_model.format_worksheet(sheet, self.start_row)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)
                                                                                        
                                    else:

                                        # Prepare the worksheet

                                        self.txtProgress.emit('Started: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')

                                        #self._pt_model.prepare_worksheet(sheet, self.start_row, 0)

                                        self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Preparing worksheet ' + sheet.title +'.')
                                        time.sleep(3)

                                        #Insert empty mapping logs

                                        key_tab = 'MINF' + '-' + sheet.title

                                        self._pt_model.append_template_logs(usage_type, 2, key_tab, [])

                                        if self._cancel_flg:return

                                success = True

                            except Exception as e:

                                self.currStatus.emit([usage_type,'Populate Worksheet',sheet.title,str(e)])

                                response = None
                                while response is None:
                                    response = self._pt_model.replyBtn
                                    time.sleep(1)

                                    if response == QMessageBox.Abort:
                                        self._abort_flg = True
                                        self._pt_model.replyBtn = None
                                        return
                                    elif response == QMessageBox.Retry:
                                        self._pt_model.replyBtn = None
                                    elif response == QMessageBox.Ignore:
                                        self._pt_model.update_template_status(usage_type, 'i')
                                        self._pt_model.replyBtn = None
                                        success = True
                                    elif response == QMessageBox.Close:
                                        self._abort_flg = True
                                        self._pt_model.replyBtn = None
                                        return

                    if self._cancel_flg:break;

                    #Update Status
                    self._pt_model.update_template_status(usage_type,'c')

                    #Price Counts

                    self.txtProgress.emit('Started: Processing '+usage_type+ ' - Generating Data Counts.')

                    if not df_price.empty and not self._abort_flg:

                        data = {'Source' : self.src_price_cnt, 'Template' : self.temp_price_cnt}
                        self._pt_model.append_template_logs(usage_type, 3, 'Price', data)

                    else:

                        
                        data = {'Source' : 0, 'Template' : 0}
                        self._pt_model.append_template_logs(usage_type, 3, 'Price', data)

                    #Scales Counts

                    if not df_scales.empty and not self._abort_flg:

                        data = {'Source' : self.src_scales_cnt, 'Template' : self.temp_scales_cnt}
                        self._pt_model.append_template_logs(usage_type, 3, 'Scales', data)

                    else:
                        data = {'Source' : 0, 'Template' : 0}
                        self._pt_model.append_template_logs(usage_type, 3, 'Scales', data)

                    #MinFee Counts

                    if not df_minf.empty and not self._abort_flg:

                        data = {'Source' : self.src_minf_cnt, 'Template' : self.temp_minf_cnt}
                        self._pt_model.append_template_logs(usage_type, 3, 'MINF', data)

                    else:
                        data = {'Source' : 0, 'Template' : 0}
                        self._pt_model.append_template_logs(usage_type, 3, 'MINF', data)

                    if self._cancel_flg:break;

                    self.txtProgress.emit('Finished: Processing '+usage_type+ ' - Generating Data Counts.')
                    time.sleep(3)

                    #Save to workbook in output folder

                    status = self._pt_model.get_template_status(usage_type)

                    if status == 'c': 
                        
                        success = False
                        while not success:
                            try:
                                self.txtProgress.emit('Started: Processing '+usage_type+ ' - Saving Workbook to Output Folder.')
                        
                                output_filename = self._tgt_folder + "\\" + template_filename

                                temp_workbook.save(output_filename)

                                self.txtProgress.emit('Started: Processing '+usage_type+ ' - Saving Workbook to Output Folder.')
                                time.sleep(3)

                                success = True
                            except Exception as e:

                                self.currStatus.emit([usage_type,'Save Template',output_filename,str(e)])

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

                self._progress_count += 1
                self.countProgress.emit(self._progress_count)
                
            ####### Program End #########

            ### Display Elapsed Time ###

            self.update_elapsed_time()

            self.txtProgress.emit('Finished')    


    def stop(self):
        self.is_running=False

    def update_elapsed_time(self):

        secs = self.timer.elapsed() / 1000
        mins = (secs / 60) % 60
        hours = (secs / 3600)
        seconds = secs % 60

        self.elapsed_time = str(hours).split('.')[0] + ' Hours ' + str(mins).split('.')[0] + ' Minutes ' + str(seconds).split('.')[0] + ' Seconds'


    def get_all_usage_types(self):
        return list(self.df_price_all.USAGE_TYPE_CD.unique())[1:]