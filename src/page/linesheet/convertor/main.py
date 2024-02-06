
import openpyxl
import pandas as pd
# import execjs
import sys
from io import StringIO

import importlib
import re
import numpy as np



class StdoutCapture:
    def __init__(self):
        self.stdout = sys.stdout
        self.captured_output = StringIO()

    def start_capture(self):
        sys.stdout = self.captured_output

    def end_capture(self):
        sys.stdout = self.stdout

    def get_output(self):
        return self.captured_output.getvalue()

# Create an instance of the StdoutCapture class
capture = StdoutCapture()

# import the time module
import time

_start_time = time.time()


def tic():
    global _start_time
    _start_time = time.time()

def tac(stage):
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60)
    print(stage+'->Time passed: {}hour:{}min:{}sec'.format(t_hour,t_min,t_sec), flush=True)

tic()
#get data from convert_linesheet.html

parent_prefix = sys.argv[2]
parent_bu = sys.argv[3]
parent_pa_id = sys.argv[4]
parent_year = sys.argv[5]
parent_month = sys.argv[6]
running = int(sys.argv[7])

product_online = sys.argv[8]
enabled_on_chanel = sys.argv[9]
# allow_cc = sys.argv[10]
# allow_cod = sys.argv[11]
new = sys.argv[10]
# allow_gift_wrapping = sys.argv[13]
allow_installment = sys.argv[11]
can_return = sys.argv[12]
can_exchange = sys.argv[13]
job_number = sys.argv[14]
# product_status = sys.argv[15]
launch_date = sys.argv[15]
sheet_name = sys.argv[16]
product_template = sys.argv[17]


# get template
channel = '-CDS'
template='pim_code'
th_identity='-th_TH'
en_identity='-en_US'
th_identity_linesheet='_th'
en_identity_linesheet='_en'
boolean_yes='1'
boolean_no='0'
ms_delimiter =','
caution_th='สีของผลิตภัณฑ์ที่แสดงบนเว็บไซต์อาจมีความแตกต่างกัน จากการตั้งค่าการแสดงผลของแต่ละหน้าจอ'
caution_en='In terms of item color, it may be slightly different from each monitor display and specification.'

# query configurable
# This function will convert the url to a download link
def convert_gsheets_url(u):
    try:
        worksheet_id = u.split('#gid=')[1]
    except:
        # Couldn't get worksheet id. Ignore it
        worksheet_id = None
    u = re.findall('https://docs.google.com/spreadsheets/d/.*?/',u)[0]
    u += 'export'
    u += '?format=csv'
    if worksheet_id:
        u += '&gid={}'.format(worksheet_id)
    return u

index_source = "https://docs.google.com/spreadsheets/d/1HbR1_zIgzYyJ-et3QWn40oAVSq8wQipwvttsnlt_Bi0/edit?#gid=1370721427"
url = convert_gsheets_url(index_source)
index = pd.read_csv(url)

attribute_setting_url = index[index['sheet_name'] == 'attribute_setting']['url'].values[0]
attribute_option_url = index[index['sheet_name'] == 'attribute_option']['url'].values[0]
categories_mapping_url = index[index['sheet_name'] == 'categories_mapping']['url'].values[0]
shipping_mapping_url = index[index['sheet_name'] == 'shipping_mapping']['url'].values[0]
color_mapping_url = index[index['sheet_name'] == 'color_mapping']['url'].values[0]
dept_subdept_mappping_url = index[index['sheet_name'] == 'dept_subdept_mappping']['url'].values[0]
jda_size_mapping_url = index[index['sheet_name'] == 'jda_size_mapping']['url'].values[0]
datapump_store_mapping_url = index[index['sheet_name'] == 'datapump_store_mapping']['url'].values[0]


# from sqlalchemy import create_engine
# cnx = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host='156.67.217.3', db="im_form", user='data_studio', pw='a417528639'))

# query = 'SELECT * FROM im_form.attribute_setting where status = "Actived" and convertor_function <> "" and  convertor_function <> "-"'
# query_configurable = pd.read_sql(query, cnx)
# original_configurable = query_configurable

url = convert_gsheets_url(attribute_setting_url)
query_configurable = pd.read_csv(url,encoding='utf-8')
query_configurable = query_configurable.fillna("")
query_configurable = query_configurable[query_configurable["convertor_function"]!=""]
query_configurable = query_configurable[query_configurable["convertor_function"]!="-"]
query_configurable = query_configurable[query_configurable["status"]=="Actived"]
original_configurable = query_configurable



# tac('Finish Query configurable data')

# loop configurable the add the column not include in linesheet
product_template_list = product_template.split(",")
query_configurable_ao_list = []
for family in product_template_list:

    query_configurable_ao_family = original_configurable[(original_configurable[family] == 'AO') | (original_configurable[family] == 'AR')]
    query_configurable_ao_list.append(query_configurable_ao_family)


# Concatenate the query results
query_configurable_ao = pd.concat(query_configurable_ao_list, ignore_index=True)
query_configurable_ao = query_configurable_ao.drop_duplicates()


# insert for other language
# Filter rows with configurable['both_language'] = True
cloned_df = query_configurable[query_configurable['both_language'] == 1]
cloned_df_ao = query_configurable_ao[query_configurable_ao['both_language'] == 1]

#add new column
query_configurable['linesheet_code_with_local'] = query_configurable['linesheet_code']
cloned_df['linesheet_code_with_local'] = cloned_df['linesheet_code']


query_configurable.loc[query_configurable['both_language']==1,'linesheet_code_with_local']= query_configurable['linesheet_code']+en_identity_linesheet
cloned_df.loc[cloned_df['both_language']==1,'linesheet_code_with_local']= cloned_df['linesheet_code']+th_identity_linesheet

query_configurable.loc[query_configurable['both_language']==1,'pim_code']= query_configurable['pim_code']+en_identity
cloned_df.loc[cloned_df['both_language']==1,'pim_code']= cloned_df['pim_code']+th_identity

query_configurable.loc[query_configurable['scopable']==1,'pim_code']= query_configurable['pim_code']+channel
cloned_df.loc[cloned_df['scopable']==1,'pim_code']= cloned_df['pim_code']+channel


# query_configurable.loc[query_configurable['pim_code_hard_header'].notnull() ,'pim_code']= query_configurable['pim_code_hard_header']
query_configurable.loc[query_configurable['pim_code_hard_header']!="" ,'pim_code']= query_configurable['pim_code_hard_header']
# cloned_df.loc[cloned_df['pim_code_hard_header'].notnull(),'pim_code']= cloned_df['pim_code_hard_header']
cloned_df.loc[cloned_df['pim_code_hard_header']!="",'pim_code']= cloned_df['pim_code_hard_header']


#add new column ao

query_configurable_ao['linesheet_code_with_local'] = query_configurable_ao['linesheet_code']
cloned_df_ao['linesheet_code_with_local'] = cloned_df_ao['linesheet_code'].copy()


# add localable
query_configurable_ao.loc[query_configurable_ao['both_language']==1,'linesheet_code_with_local']= query_configurable_ao['linesheet_code']+en_identity_linesheet
cloned_df_ao.loc[cloned_df_ao['both_language']==1,'linesheet_code_with_local']= cloned_df_ao['linesheet_code']+th_identity_linesheet

query_configurable_ao.loc[query_configurable_ao['both_language']==1,'pim_code']= query_configurable_ao['pim_code']+en_identity
cloned_df_ao.loc[cloned_df_ao['both_language']==1,'pim_code']= cloned_df_ao['pim_code']+th_identity

# add scopable
query_configurable_ao.loc[query_configurable_ao['scopable']==1,'pim_code']= query_configurable_ao['pim_code']+channel
cloned_df_ao.loc[cloned_df_ao['scopable']==1,'pim_code']= cloned_df_ao['pim_code']+channel

# hard_code_column name
# query_configurable_ao.loc[query_configurable_ao['pim_code_hard_header'].notnull(),'pim_code']= query_configurable_ao['pim_code_hard_header']
query_configurable_ao.loc[query_configurable_ao['pim_code_hard_header']!="",'pim_code']= query_configurable_ao['pim_code_hard_header']
# cloned_df_ao.loc[cloned_df_ao['pim_code_hard_header'].notnull(),'pim_code']= cloned_df_ao['pim_code_hard_header']
cloned_df_ao.loc[cloned_df_ao['pim_code_hard_header']!="",'pim_code']= cloned_df_ao['pim_code_hard_header']


# Concatenate the original and cloned dataframes
configurable = pd.concat([query_configurable, cloned_df], ignore_index=True)
configurable_ao_fame = pd.concat([query_configurable_ao, cloned_df_ao], ignore_index=True)





# query = 'SELECT linesheet_code,input_option,option_code,option_th,option_en FROM u749625779_cdscontent.pim_attr_convert_option_lu'
# mapping_option_value = pd.read_sql(query, cnx)

url = convert_gsheets_url(attribute_option_url)
mapping_option_value = pd.read_csv(url)
mapping_option_value = mapping_option_value[['linesheet_code','input_option','option_code','option_th','option_en']]



# query = 'SELECT label_th, full_categories_code , family , size_value_template , product_name_template_th  ,product_name_template_en,description_block_template FROM im_form.categories_setting;'
# categories_mapping = pd.read_sql(query, cnx)

url = convert_gsheets_url(categories_mapping_url)
categories_mapping = pd.read_csv(url)
categories_mapping = categories_mapping[['label_th','full_categories_code','family','size_value_template','product_name_template_th','product_name_template_en','description_block_template']]


# query = 'SELECT brand_group, one_hr, tree_hr FROM u749625779_cdscontent.shipping_mapping where one_hr  = "Yes";'
# shipping_mapping_one_hr = pd.read_sql(query, cnx)

url = convert_gsheets_url(shipping_mapping_url)
shipping_mapping_one_hr = pd.read_csv(url)
shipping_mapping_one_hr = shipping_mapping_one_hr[['brand_group','one_hr','tree_hr']]
shipping_mapping_one_hr = shipping_mapping_one_hr[shipping_mapping_one_hr['one_hr']=="Yes"]

# query = 'SELECT brand_group, one_hr, tree_hr FROM u749625779_cdscontent.shipping_mapping where tree_hr  = "Yes";'
# shipping_mapping_tree_hr = pd.read_sql(query, cnx)

url = convert_gsheets_url(shipping_mapping_url)
shipping_mapping_tree_hr = pd.read_csv(url)
shipping_mapping_tree_hr = shipping_mapping_tree_hr[['brand_group','one_hr','tree_hr']]
shipping_mapping_tree_hr = shipping_mapping_tree_hr[shipping_mapping_tree_hr['tree_hr']=="Yes"]

# query = 'SELECT attribute_code,input_option,option_code,option_th,option_en,color_group_pim_code FROM im_form.color_mapping'
# color_mapping = pd.read_sql(query, cnx)

url = convert_gsheets_url(color_mapping_url)
color_mapping = pd.read_csv(url)
color_mapping = color_mapping[['attribute_code','input_option','option_code','option_th','option_en','color_group_pim_code']]



# create new excel template
global workbook
global worksheet
global ws_template
global ws_model

global pim_code
global linesheet_code

workbook = openpyxl.Workbook()
worksheet = workbook.active

# worksheet.title = 'template'
# ws_template = workbook['template']

# get configurable
linesheet_code = configurable['linesheet_code'].values.tolist()
configurable_ao = configurable_ao_fame['linesheet_code_with_local'].values.tolist()
# configurable_ao = configurable_ao['linesheet_code_with_local'].values.tolist()
# linesheet_list = configurable['linesheet_code'].values.tolist()
linesheet_code_with_local = configurable['linesheet_code_with_local'].values.tolist()
template_code = configurable[template].values.tolist()
both_language = configurable['both_language'].values.tolist()
convertor_function = configurable['convertor_function'].values.tolist()
label_desc_en= configurable['label_desc_en'].values.tolist()
label_desc_th= configurable['label_desc_th'].values.tolist()
linesheet_code_unit= configurable['linesheet_code_unit'].values.tolist()
shipping_mapping_one_hr=shipping_mapping_one_hr['brand_group'].values.tolist()
shipping_mapping_tree_hr=shipping_mapping_tree_hr['brand_group'].values.tolist()
scopable= configurable['scopable'].values.tolist()


# print(configurable_ao,flush=True)
# tac('Finnish data transformation')
# create a dictionary where the keys are the values in the linesheet_code list
# and the values are empty lists
data = {code: [] for code in template_code}

# Create an empty DataFrame with the column headers from the list
ws_template = pd.DataFrame(columns=template_code)
ws_template.columns

ws_model = pd.DataFrame(columns=template_code)
ws_model.columns
# insert function
info = []
error = []
warning = []

## read linesheet
import xlrd
import openpyxl

import sys
import pandas as pd


# Read JSON file path from command line argument
file_path_json = sys.argv[1]

# Read the JSON file into a DataFrame
linesheet = pd.read_json(file_path_json)
# Reset the index
# linesheet = linesheet.set_index([pd.Index(['index_columns'])])

# linesheet.reset_index()
# linesheet = linesheet.to_string(index=False)


# linesheet.to_csv('linesheet_set.csv')
linesheet = linesheet.reset_index(drop=True)
linesheet = linesheet.astype(str)

# tac('Reading the file..')
# print(linesheet)

# print('Read file successfully')

# linesheet = pd.read_excel('./app/convertor/CDS2301-0341 NS-18608 ANGEL BABY 31 SKUs Buyerfile.xlsm',index_col=False,dtype='string')
original_linesheet=linesheet
linesheet_columns= linesheet.columns.tolist()

linesheet = linesheet.fillna("")


# create a list of column names that do not contain "Unnamed"
cols = [col for col in linesheet.columns if 'Unnamed' not in col]

# select only the columns that do not contain "Unnamed"
linesheet = linesheet[cols]

# replace version[hard_code]
linesheet = linesheet.rename(columns={"product_detail_en" : "product_information_en"})
linesheet = linesheet.rename(columns={"product_detail_th" : "product_information_th"})

# linesheet = linesheet.rename(columns={"product_information_en" : "description_en"})
# linesheet = linesheet.rename(columns={"product_information_th" : "description_th"})



# drop rows 2-13
# linesheet = linesheet.drop(index=range(0,11))

##-------end read excel
from f_function import *
from f_convert import *

# remove old file

try:
    remove_excel_file('converted/template.xlsx')
    remove_excel_file('converted/model.xlsx')
except:
    print('.')

# create an empty dictionary to store variables
my_dict = {}

# add all global variables to the dictionary
for var_name, var_value in list(globals().items()):
    my_dict[var_name] = var_value

# create a dictionary mapping column names to functions
function_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['convertor_function']))
template_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['pim_code']))
common_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['grouping_common']))
# scopable_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['scopable']))

# create column set for looping to convert
linesheet_columns = linesheet.columns.tolist()
convert_column = configurable_ao+linesheet_columns

# Add new columns to the DataFrame
linesheet = pd.DataFrame(linesheet, columns=linesheet.columns.tolist() + configurable_ao)
linesheet = linesheet.loc[:, ~linesheet.columns.duplicated()]
linesheet.to_csv('linesheet.csv')
# loop in linesheet then apply the functions to the columns
for linesheet_code in convert_column:

    # tac('End '+linesheet_code+' convert')

    if linesheet_code not in function_dict:
        linesheet = linesheet.drop(linesheet_code, axis=1)
    else:
        func_call =  globals()[function_dict[linesheet_code]]
        var_type = common_dict[linesheet_code]
        # scopable_type = scopable_dict[linesheet_code]

        try:

            linesheet[linesheet_code] = linesheet.apply(func_call,axis=1, args=(linesheet_code,my_dict))
        except Exception as err:

            print('Warning : '+linesheet_code+' at function : '+str(function_dict[linesheet_code])+' '+str(err), flush=True)

        pim_code = template_dict[linesheet_code]

        try:
            # if linesheet['group_by']=='':
            ws_template[pim_code]=linesheet[linesheet_code]
            # if 'variant' in var_type:
            #     ws_template[pim_code]=linesheet[linesheet_code]
            if 'common' in var_type:
                ws_model[pim_code]=linesheet[linesheet_code]
                # also add to template for non grouping

            if 'variant' not in var_type and 'common' not in var_type:
                error.append('Error : missing variant configurable for '+pim_code)
                print('Error : missing variant configurable for '+pim_code, flush=True)


            info.append('Processing ..' + pim_code)

        except Exception as err:
            warning.append('Warning : linesheet have no attribute '+pim_code)
            print('Warning : '+pim_code+' '+str(err), flush=True)

# == grouping a product
parent_info = {
    'parent_prefix': parent_prefix,
    'parent_bu': parent_bu,
    'parent_pa_id': parent_pa_id ,
    'parent_year': parent_year,
    'parent_month': parent_month,
    'running': running
}

ws_template = add_parent_column(ws_template, **parent_info)
ws_model = add_parent_column(ws_model, **parent_info)
original_linesheet = add_parent_column(original_linesheet, **parent_info)






# tac('Finish grouping')
# remove duplicates for model file
ws_model = ws_model.drop_duplicates()
ws_model = ws_model[ws_model['group_by-CDS']!='']

#add visibility of product
# ws_model['visibility-CDS']= 'Catalog__Search'
# ws_template['visibility-CDS']= 'Not_Visible_Individually'


# Before adding the 'visibility-CDS' column, create a new DataFrame with the column
new_columns = pd.concat([ws_template, pd.Series(['Not_Visible_Individually'] * len(ws_template), name='visibility-CDS')], axis=1)
new_columns.loc[new_columns['parent'] != '', 'visibility-CDS'] = 'Not_Visible_Individually'
ws_template = new_columns

new_columns = pd.concat([ws_template, pd.Series(['Catalog__Search'] * len(ws_template), name='visibility-CDS')], axis=1)
new_columns.loc[new_columns['parent'] == '', 'visibility-CDS'] = 'Catalog__Search'
ws_template = new_columns

# ws_template.loc[ws_template['parent']!='','visibility-CDS']='Not_Visible_Individually'
# ws_template.loc[ws_template['parent']=='','visibility-CDS']='Catalog__Search'

if not ws_model.empty:
    ws_model.loc[ws_model['brand_name-CDS']=='CHANEL','visibility-CDS']='Catalog__Search'
    ws_model.loc[ws_model['brand_name-CDS']!='CHANEL','visibility-CDS']='Catalog__Search'



# remove empty columns using the updated drop_empty_columns function
ws_template = ws_template.fillna('')
ws_model = ws_model.fillna('')
linesheet = linesheet.fillna('')

ws_template = ws_template.astype(str)
ws_model = ws_model.astype(str)
linesheet = linesheet.astype(str)

ws_template = remove_empty_columns(ws_template)
ws_model = remove_empty_columns(ws_model)
# tac('Finish remove empty column !')




import os

folder_name = "converted"
path = os.path.join(os.getcwd(), folder_name)

os.makedirs("converted" , exist_ok=True)




# rename and positioning for parent column in model template
# Check if the DataFrame is empty
if ws_model.empty:
    # tac('Info : No grouping')
    ws_template = ws_template.rename(columns={'catalogue_number_for_group': 'catalog_no'})
else:

    #replace product name with original from linesheet
    ws_model = replace_column_values_with_lookup(ws_model, original_linesheet, 'name-en_US-CDS', 'parent', 'parent' , 'product_name_en')
    ws_model = replace_column_values_with_lookup(ws_model, original_linesheet, 'name-th_TH-CDS', 'parent', 'parent' , 'product_name_th')
    ws_model = replace_column_values_with_lookup(ws_model, original_linesheet, 'group_name-CDS', 'parent', 'parent' , 'product_name_en')

    ws_model = rename_parent_column_and_move_positioning(ws_model)
    ws_template = move_positioning_template(ws_template)

    ws_model = ws_model.rename(columns={'catalogue_number_for_group': 'catalog_no'})
    ws_template = ws_template.rename(columns={'catalogue_number_for_group': 'catalog_no'})


    ws_template = ws_template.drop('family_variant', axis=1)
    ws_model.to_excel("converted/model.xlsx",index=False)


# tac('Finish packing')

linesheet.to_excel("converted/linesheet.xlsx" ,index=False)
original_linesheet.to_excel("converted/original_linesheet.xlsx" ,index=False)
ws_template.to_excel("converted/template.xlsx" ,index=False)


# try:
#     os.mkdir(path)
#     print(f"Folder '{folder_name}' created successfully!")
# except FileExistsError:
#     print(f"Folder '{folder_name}' already exists.")
# except Exception as e:
#     print(f"An error occurred while creating folder '{folder_name}': {e}")


# linesheet.to_excel("converted/linesheet.xlsx",index=False)

tac('Success : Finish Convert !')

# import os
# folder_path_os = os.path.abspath('converted')
# folder_path_os = folder_path_os.replace('\\', '\\\\')

# print('''

# ''')

# print the DataFrame
# print(ws_model.head(10).to_string(index=False))
# ws_template.to_csv('template.csv' , index=False , encoding='utf-8')
# linesheet.to_csv('linesheet.csv',index=False , encoding='utf-8')

# ws_template.to_excel("template.xlsx")
# linesheet.to_excel("linesheet.xlsx")


# print(warning+error)
