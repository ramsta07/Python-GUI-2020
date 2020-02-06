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


                Check if List Prices, CAP, MINQ and Flight to be populated

                '''

                for conf in self._pt_model._usageflow_conf:

                    if conf['UsageType'] == usage_type:

                        self.isListPrice = conf['IsListPrices']
                        self.isCAP = conf['IsCAP']
                        self.isFlight = conf['IsFlight']
                        self.isMINQ = conf['IsMINQ']

                        break;

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
                        'fld_Bill_To': 'fld_Bill-To',
                        'fld_Requestor': 'fld_Requester', 
                        'fld_Price': 'fld_Price_Amount', 
                        'fld_Pricing_Bundle_ID': 'fld_Bundle_ID',
                        'fld_Pricing_Contract_Type': 'fld_Contract_Type', 
                        'fld_Pricing_Contract_SubType': 'fld_Contract_Sub_Type',
                        'fld_Maximum_Take_Off_Weight_Range': 'fld_MTOW_Range',
                        'fld_Stock_Type': 'fld_Stock_Ticket_Type',
                        'fld_Public_Mode': 'fld_Publication_Mode',
                        'fld_Special_Price_Element': 'fld_Special_pricing_element',
                        'fld_Hotel_Property_City': 'fld_Hotel_Property_&_City',
                        'fld_Priodicity': 'fld_Periodicity',
                        'fld_Flight_Range_Code': 'fld_Flight_Range'}, inplace=True)

                    # Add columns to dataframe

                    df_price['fld_Dist_Channel'] = df_price['fld_Distribution_Channel']
                    df_price['fld_Off_Country'] = df_price['fld_Office_Country']
                    df_price['fld_Off_Owner'] = df_price['fld_Office_Owner']
                    df_price['fld_Off_Group'] = df_price['fld_Office_Group']
                    df_price['fld_Reach_Ind'] = df_price['fld_Reach_Indicator']
                    df_price['fld_Old_Material_Group'] = df_price['fld_Material_Group']
                    df_price['fld_Bkg_Channel'] = df_price['fld_Original_Booking_Channel']
                    df_price['fld_Accp_channel'] = df_price['fld_Acceptance_Channel']
                    df_price['fld_Prod_Channel'] = df_price['fld_Product_Channel']
                    df_price['fld_Shared_Scale_ID'] = df_price['fld_SSCALE_ID']
                    df_price['fld_Shared_Scale_BP'] = df_price['fld_SSCALE_BP']
                    df_price['fld_Departure_Airport'] = '*'
                    df_price['fld_Coupons_Status'] = df_price['fld_Coupon_Status']
                    df_price['fld_Group_Bkgs'] = df_price['fld_Group_Booking']
                    df_price['fld_Mkt_Carrier'] = df_price['fld_Marketing_Carrier']
                    df_price['fld_Flight_Range_Code'] = df_price['fld_Flight_Range']

                    # Common Audit Fields

                    df_price['fld_Created_By'] = ''
                    df_price['fld_Last_Upd'] = ''
                    df_price['fld_Last_Upd_By'] = 'DATA MIG'
                    df_price['fld_Created'] = ''

                    self.txtProgress.emit('Processing {} - Filtering and Validating dataframe.'.format(usage_type))

                    #Loop on the template worksheet

                    for sheet in temp_worksheets:

                        self.ws_name = sheet.name.lower()

                        success = False
                        while not success:

                            try:

                                if 'flight' in self.ws_name:
                                    self.start_row = 3
                                else:
                                    self.start_row = self._pt_model._config['StartRow']

                                if ('price' in self.ws_name and 'scale' not in self.ws_name) or ('minq' in self.ws_name or 'caps' in self.ws_name or 'flight' in self.ws_name): 

                                    self.src_price_cnt = df_price.shape[0]

                                    if not df_price.empty and not self._cancel_flg:

                                        if 'customer' in self.ws_name:

                                            self.temp_price_cnt = self.populate_price_tabs(usage_type, sheet, df_price, 'Price', self.start_row, self.src_price_cnt)

                                        elif self.isListPrice:

                                            self.populate_price_tabs(usage_type, sheet, df_price, 'Price', self.start_row, self.src_price_cnt)

                                        elif (self.isCAP or self.isMINQ):

                                            # Mappings for CAP, Flight range and MINQ

                                            self.txtProgress.emit('Started: Processing {} - Additional mappings for {}.'.format(usage_type, sheet.name))

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

                                            self.txtProgress.emit('Finished: Processing {} - Additional mappings for {}.'.format(usage_type, sheet.name))
                                            time.sleep(3)
                                            
                                            self.populate_price_tabs(usage_type, sheet, df_price, 'Price', self.start_row, self.src_price_cnt)
                                            
                                        elif self.isFlight:

                                            df_price['fld_ID'] = '*'
                                            df_price['fld_Lower_Bound'] = '*'
                                            df_price['fld_Upper_Bound'] = '*'
                                            df_price['fld_Flight_Range_Code'] =  df_price['fld_Flight_Range']
                                            df_price['fld_Flight_Range_Label'] = '*'

                                            self.populate_price_tabs(usage_type, sheet, df_price, 'Price', self.start_row, self.src_price_cnt)
                                        
                                        else:

                                            self.clear_worksheet(usage_type, sheet, self.start_row, 'Price')
                                    else:

                                        self.clear_worksheet(usage_type, sheet, self.start_row, 'Price')
                                        
                                        if self._cancel_flg:return;

                                elif 'scale' in self.ws_name:

                                    if not df_scales.empty and not self._cancel_flg:

                                        #Merge DataFrame with Price DataFrame

                                        self.txtProgress.emit('Started: Processing {} - Merging scales dataframe to Price.'.format(usage_type))

                                        merged_price_scale_df = self._pt_model.merge_scale_price_df(df_scales, df_price)

                                        self.txtProgress.emit('Finished: Processing {} - Merging scales dataframe to Price.'.format(usage_type))
                                        time.sleep(3)

                                        if merged_price_scale_df.shape[0] != 0:
                                        
                                            # Mapping logic for Type of calendar and reference_date

                                            self.txtProgress.emit('Started: Processing {} - Applying additional scales logic.'.format(usage_type))

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
                                            
                                            self.txtProgress.emit('Finished: Processing {} - Applying additional scales logic.'.format(usage_type))
                                            time.sleep(3)
                                            
                                            self.src_scales_cnt = merged_price_scale_df.shape[0]

                                            self.temp_scales_cnt = self.populate_price_tabs(usage_type, sheet, merged_price_scale_df, 'Scales', self.start_row, self.src_scales_cnt)

                                        else:

                                            self.clear_worksheet(usage_type, sheet, self.start_row, 'Scales')

                                    else:

                                        self.clear_worksheet(usage_type, sheet, self.start_row, 'Scales')

                                        if self._cancel_flg:return
    
                                elif 'minf' in self.ws_name:

                                    if not df_minf.empty and not self._cancel_flg:

                                        if set(['fld_Counter_ID', 'fld_Frequency', 'fld_Type_of_Calendar', 'fld_Reference_Date', 'fld_Billing_Material']).issubset(df_price.columns):

                                            self.txtProgress.emit('Started: Processing {} - Preparing MINQ dataframe.'.format(usage_type))

                                            # Drop not needed columns added on price dataframe

                                            df_price.drop(['fld_Counter_ID', 'fld_Frequency', 'fld_Type_of_Calendar', 'fld_Reference_Date', 'fld_Billing_Material'], axis=1, inplace=True)

                                            self.txtProgress.emit('Finished: Processing {} - Preparing MINQ dataframe.'.format(usage_type))
                                            time.sleep(3)
                                                
                                        #Merge DataFrame with Price DataFrame
                                        
                                        self.txtProgress.emit('Started: Processing {} - Merging MINF dataframe to Price.'.format(usage_type))

                                        df_price_req = df_price[['Short_Text_Key','fld_Business_Partner','HybrisProduct_ID','fld_OTC_Billing_Material_ID','fld_MF_Counter',
                                                                'fld_Discount','fld_Discount_Type','fld_Discount_Description','fld_Item_Category']]
                                    
                                        #Merge DataFrame with Price DataFrame

                                        merged_price_minf_df = self._pt_model.merge_minf_price_df(df_minf, df_price_req)

                                        if merged_price_minf_df.shape[0] != 0:

                                            #Rename columns
                                            merged_price_minf_df.rename(columns={
                                                                    'Start_Date':'fld_Reference_Date',
                                                                    'Frequency': 'fld_Frequency',
                                                                    'Currency':'fld_Currency',
                                                                    'fld_OTC_Billing_Material_ID': 'fld_Billing_Material',
                                                                    'Minimum_Fee':'fld_Min_Fee',
                                                                    'fld_MF_Counter':'fld_Counter_ID',},inplace=True)
                                            
                                            merged_price_minf_df['fld_Type_of_Calendar'] = '*'

                                            self.txtProgress.emit('Finished: Processing {} - Merging MINF dataframe to Price.'.format(usage_type))
                                            time.sleep(3)
                                            
                                            self.src_minf_cnt = merged_price_minf_df.shape[0]

                                            self.temp_minf_cnt = self.populate_price_tabs(usage_type, sheet, merged_price_minf_df, 'MINF', self.start_row, self.src_minf_cnt)

                                        else:


                                            self.clear_worksheet(usage_type, sheet, self.start_row, 'MINF')

                                    else:

                                        self.clear_worksheet(usage_type, sheet, self.start_row, 'MINF')

                                        if self._cancel_flg:return

                                success = True

                            except Exception as e:

                                self.currStatus.emit([usage_type,'Populate Worksheet',sheet.name,str(e)])

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

                    self.txtProgress.emit('Started: Processing {} - Generating Data Counts.'.format(usage_type))

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

                    self.txtProgress.emit('Finished: Processing {} - Generating Data Counts.'.format(usage_type))
                    time.sleep(3)

                    #Save to workbook in output folder

                    status = self._pt_model.get_template_status(usage_type)

                    if status == 'c': 
                        
                        success = False
                        while not success:
                            try:
                                self.txtProgress.emit('Started: Processing {} - Saving Workbook to Output Folder.'.format(usage_type))
                        
                                output_filename = self._tgt_folder + "\\" + template_filename

                                temp_workbook.save(output_filename)
                                temp_workbook.close()

                                self.txtProgress.emit('Finished: Processing {} - Saving Workbook to Output Folder.'.format(usage_type))
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

                    else:

                        temp_workbook.close()

                self._progress_count += 1
                self.countProgress.emit(self._progress_count)
                
            ####### Program End #########

            ### Display Elapsed Time ###

            self.update_elapsed_time()

            self.txtProgress.emit('Finished')    

    def populate_price_tabs(self, usage_type, sheet, df, tab, start_row, src_cnt):

        # Get Mappings

        self.txtProgress.emit('Started: Processing {} - Getting mappings for {}.'.format(usage_type, sheet.name))

        l_mapping = self._pt_model.get_template_mappings(usage_type, sheet, df, tab)

        self.txtProgress.emit('Finished: Processing {} - Getting mappings for {}.'.format(usage_type, sheet.name))
        time.sleep(3)

        # Prepare the worksheet

        self.txtProgress.emit('Started: Processing {} - Preparing worksheet {}.'.format(usage_type, sheet.name))

        self._pt_model.prepare_worksheet(sheet, start_row, src_cnt)

        self.txtProgress.emit('Finished: Processing {} - Preparing worksheet {}.'.format(usage_type, sheet.name))
        time.sleep(3)

        # Populate data from dataframe to worksheet

        self.txtProgress.emit('Started: Processing {} - Populating worksheet {}.'.format(usage_type, sheet.name))

        temp_count = self._pt_model.populate_worksheet(sheet, df, l_mapping, start_row)

        self.txtProgress.emit('Finished: Processing {} - Populating worksheet {}.'.format(usage_type, sheet.name))
        time.sleep(3)

        return temp_count

    def clear_worksheet(self, usage_type, sheet, start_row, tab):

        # Prepare the worksheet

        self.txtProgress.emit('Started: Processing {} - Clearing worksheet {}.'.format(usage_type, sheet.name))

        self._pt_model.prepare_worksheet(sheet, start_row, 0)

        self.txtProgress.emit('Finished: Processing {} - Clearing worksheet {}.'.format(usage_type, sheet.name))
        time.sleep(3)
                    
        #Insert empty mapping logs

        key_tab = tab + '-' + sheet.name

        self._pt_model.append_template_logs(usage_type, 2, key_tab, [])

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