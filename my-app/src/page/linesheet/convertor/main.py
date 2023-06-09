
import openpyxl
import pandas as pd

# get template
template='pim_code'
th_identity='-th_TH'
en_identity='-en_US'
th_identity_linesheet='_th'
en_identity_linesheet='_en'
boolean_yes='TRUE'
boolean_no='FALSE'
ms_delimiter =','
caution_th='สีของผลิตภัณฑ์ที่แสดงบนเว็บไซต์อาจมีความแตกต่างกัน จากการตั้งค่าการแสดงผลของแต่ละหน้าจอ'
caution_en='In terms of item color, it may be slightly different from each monitor display and specification.'

# query configurable
from sqlalchemy import create_engine
cnx = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host='156.67.217.3', db="im_form", user='data_studio', pw='a417528639'))

query = 'SELECT * FROM im_form.attribute_setting where status = "Actived" and convertor_function <> "" and  convertor_function <> "-"'
query_configurable = pd.read_sql(query, cnx)

# insert for other language
# Filter rows with configurable['both_language'] = True
cloned_df = query_configurable[query_configurable['both_language'] == 'true']

#add new column
query_configurable['linesheet_code_with_local'] = query_configurable['linesheet_code']
cloned_df['linesheet_code_with_local'] = cloned_df['linesheet_code']

query_configurable.loc[query_configurable['both_language']=='true','linesheet_code_with_local']= query_configurable['linesheet_code']+en_identity_linesheet
cloned_df.loc[cloned_df['both_language']=='true','linesheet_code_with_local']= cloned_df['linesheet_code']+th_identity_linesheet

query_configurable.loc[query_configurable['both_language']=='true','pim_code']= query_configurable['pim_code']+en_identity
cloned_df.loc[cloned_df['both_language']=='true','pim_code']= cloned_df['pim_code']+th_identity

# Concatenate the original and cloned dataframes
configurable = pd.concat([query_configurable, cloned_df], ignore_index=True)

query = 'SELECT linesheet_code,input_option,option_code,option_th,option_en FROM u749625779_cdscontent.pim_attr_convert_option_lu'
mapping_option_value = pd.read_sql(query, cnx)

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
# linesheet_list = configurable['linesheet_code'].values.tolist()
linesheet_code_with_local = configurable['linesheet_code_with_local'].values.tolist()
template_code = configurable[template].values.tolist()
both_language = configurable['both_language'].values.tolist()
convertor_function = configurable['convertor_function'].values.tolist()
label_desc_en= configurable['label_desc_en'].values.tolist()
label_desc_th= configurable['label_desc_th'].values.tolist()


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
file_path = sys.argv[1]

# Read the JSON file into a DataFrame
linesheet = pd.read_json(file_path)
# Reset the index
linesheet = linesheet.reset_index(drop=True)
linesheet = linesheet.astype(str)

print('Read file successfully')

# linesheet = pd.read_excel('./app/convertor/CDS2301-0341 NS-18608 ANGEL BABY 31 SKUs Buyerfile.xlsm',index_col=False,dtype='string')
original_linesheet=linesheet
linesheet_columns= linesheet.columns.tolist()

linesheet = linesheet.fillna("")

# create a list of column names that do not contain "Unnamed"
cols = [col for col in linesheet.columns if 'Unnamed' not in col]

# select only the columns that do not contain "Unnamed"
linesheet = linesheet[cols]

# replace version[hard_code]
linesheet = linesheet.rename(columns={"product_detail_en" : "description_en"})
linesheet = linesheet.rename(columns={"product_detail_th" : "description_th"})

# drop rows 2-13
# linesheet = linesheet.drop(index=range(0,11))

##-------end read excel
from f_function import *
from f_convert import *

# create an empty dictionary to store variables
my_dict = {}

# add all global variables to the dictionary
for var_name, var_value in list(globals().items()):
    my_dict[var_name] = var_value

# create a dictionary mapping column names to functions
function_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['convertor_function']))
template_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['pim_code']))
common_dict = dict(zip(configurable['linesheet_code_with_local'], configurable['grouping_common']))


# apply the functions to the columns
for linesheet_code in linesheet.columns:
    if linesheet_code not in function_dict:
        linesheet = linesheet.drop(linesheet_code, axis=1)
    else:
        func = function_dict[linesheet_code]
        var_type = common_dict[linesheet_code]


        if  func != 'categories' and func != 'categories full path' :
            func_call =  globals()[func]
            print(func_call)
            linesheet[linesheet_code] = linesheet.apply(func_call,axis=1, args=(linesheet_code,my_dict))

        pim_code = template_dict[linesheet_code]

        try:
            if 'variant' in var_type:
                ws_template[pim_code]=linesheet[linesheet_code]
            if 'common' in var_type:
                ws_model[pim_code]=linesheet[linesheet_code]
            if 'variant' not in var_type and 'common' not in var_type:
                 print('missing variant in setting for '+pim_code)

            print('Processing ..' + pim_code)
        except:
            print('warning : linesheet have no attribute '+pim_code)


# == grouping a product
parent_info = {
    'parent_prefix': 'GR',
    'parent_bu': 'CDS',
    'parent_pa_id': '01',
    'parent_year': '05',
    'parent_month': '10',
    'running': 1
}

print('grouping ..')
ws_template = add_parent_column(ws_template, **parent_info)
ws_model = add_parent_column(ws_model, **parent_info)

# remove duplicates for model file
ws_model = ws_model.drop_duplicates()


# remove empty columns using the updated drop_empty_columns function
ws_template = remove_empty_columns(ws_template)
ws_model = remove_empty_columns(ws_model)


# rename and positioning for parent column in model template
ws_model = rename_parent_column_and_move_positioning(ws_model)

print('packing ..')
ws_template.to_excel("template.xlsx" ,index=False)
ws_model.to_excel("model.xlsx",index=False)
linesheet.to_excel("linesheet.xlsx",index=False)
print('packed ..')

# print the DataFrame
# print(ws_model.head(10).to_string(index=False))
# ws_template.to_csv('template.csv' , index=False , encoding='utf-8')
# linesheet.to_csv('linesheet.csv',index=False , encoding='utf-8')

# ws_template.to_excel("template.xlsx")
# linesheet.to_excel("linesheet.xlsx")


print(info)

