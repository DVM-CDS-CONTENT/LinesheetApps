import mysql.connector
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sre_compile

def get_family():

    engine = create_engine('mysql+mysqlconnector://data_studio:a417528639@156.67.217.3/im_form')
    # cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = 'SELECT * FROM im_form.attribute_setting order by session,sub_session,id'
    attribute = pd.read_sql(query, engine)

    columns = attribute.columns.tolist()
    columns_to_exclude = ['id', 'information_type', 'status', 'enhancement', 'specific_brand', 'linesheet_code', 'field_label', 'field_type', 'both_language', 'description', 'tool_tips', 'session', 'sub_session', 'merge_group', 'sale_channel', 'formula', 'pim_code', 'convertor_function', 'linesheet_code_unit', 'label_desc_en', 'label_desc_th', 'value_desc_format', 'sort_bullet_point', 'grouping_common']
    columns_to_include = [value for value in columns if value not in columns_to_exclude]
    options = ''.join([f'<option value="{value}">{value}</option>' for value in columns_to_include])
    html = f'''
            <label for="stock_source" class="text-black mb-2 mt-2">Template</label>

            <input type="hidden" id="template" name="template" value="">
            <select multiple id="template_show" name="template_show" aria-label="stock_source" class="">
                {options}
            </select>
    '''
    return html

def get_input(attribute, type):
    # cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    engine = create_engine('mysql+mysqlconnector://data_studio:a417528639@156.67.217.3/im_form')
    query = f'SELECT * FROM u749625779_cdscontent.job_attribute_option where attribute_table="add_new_job" and attribute_code = "{attribute}"'
    input_value = pd.read_sql(query, engine)
    input_value['option_group'] = input_value['option_group'].fillna(input_value['attribute_code'])
    input_group = np.unique(input_value['option_group'].tolist())
    optgroup = ''
    for group in input_group:
        input_value_filter = input_value[input_value['option_group']==group]
        input_list = input_value_filter['attribute_option_code'].tolist()
        default_option = [option.replace("yes", "selected").replace("no", "") for option in input_value_filter['default_option'].tolist()]
        default_option_list = [value for i, value in enumerate(input_list) if default_option[i]=='selected']
        options = ''.join([f'<option {default_option[i]} value="{value}">{value}</option>' for i, value in enumerate(input_list)])
        default_option_str= ",".join(default_option_list)
        optgroup += f'<optgroup label="{group}" data-selectall="true">{options}</optgroup>'
    html = f'''
            <label for="stock_source" class="text-black mb-2 mt-2">{attribute}</label>

            <input type="hidden" id="{attribute}" name="{attribute}" value="{default_option_str}">
            <select {type} id="{attribute}_show" name="{attribute}_show" class="" aria-label="{attribute}">
                {optgroup}
            </select>

    '''
    return html



# two grid get input
def get_text_input_two_grid(attribute, input_type,default_option_str,row):
  if  input_type =='free_text':
            html = f'''

                <div class="row p-1">
                    <div class="col-4" style="display: grid;">
                        <span>{attribute}</span>
                    </div>
                    <div class="col-8">
                        <input type="text" id="{attribute}" onChange="updateExcelCellValue('IN_LINK_DATA', 1, {row}, '{attribute}');" value="{default_option_str}" class="form-control" placeholder="">
                    </div>
                </div>

        '''

  return html

def get_multi_select_input_two_grid(attribute, input_type,default_option_str,row):

    engine = create_engine('mysql+mysqlconnector://data_studio:a417528639@156.67.217.3/im_form')
    # cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = f'SELECT * FROM u749625779_cdscontent.job_attribute_option where attribute_table="add_new_job" and attribute_code = "{attribute}"'
    input_value = pd.read_sql(query, engine)
    input_value['option_group'] = input_value['option_group'].fillna(input_value['attribute_code'])
    input_group = np.unique(input_value['option_group'].tolist())
    optgroup = ''
    for group in input_group:
        input_value_filter = input_value[input_value['option_group']==group]
        input_list = input_value_filter['attribute_option_code'].tolist()

        if "," in default_option_str:
            default_option = ["selected" if val in input_list else "" for val in default_option_str.split(",") if val]
        else:
            default_option = ['selected' if default_option_str == val else '' for val in input_list]



        options = ''.join([f'<option {default_option[i]} value="{value}">{value}</option>' for i, value in enumerate(input_list)])
        optgroup += f'<optgroup label="{group}" data-selectall="true">{options}</optgroup>'

        html = f'''

            <div class="row p-1">
                <div class="col-4" style="display: grid;">
                    <span>{attribute}</span>
                </div>
                <div class="col-8">
                    <input type="hidden" id="{attribute}" value="{default_option_str}"class="form-control" placeholder="">
                    <select  {input_type}  id="{attribute}_show" name="{attribute}_show" class="" aria-label="{attribute}" onChange="updateExcelCellValue('IN_LINK_DATA', 1, '{row}', '{attribute}_show');">
                        {optgroup}
                    </select>
                </div>
            </div>

            '''

    return html

def get_single_select_input_two_grid(attribute, input_type,default_option_str,row):
    engine = create_engine('mysql+mysqlconnector://data_studio:a417528639@156.67.217.3/im_form')
    # cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = f'SELECT * FROM u749625779_cdscontent.job_attribute_option where attribute_table="add_new_job" and attribute_code = "{attribute}"'
    input_value = pd.read_sql(query, engine)
    input_value['option_group'] = input_value['option_group'].fillna(input_value['attribute_code'])
    input_group = np.unique(input_value['option_group'].tolist())
    optgroup = ''
    default_option=[]
    for group in input_group:
        input_value_filter = input_value[input_value['option_group']==group]
        input_list = input_value_filter['attribute_option_code'].tolist()
        default_option = ['selected' if default_option_str == val else '' for val in input_list]
        options = ''.join([f'<option {(default_option[i])} value="{value}">{value}</option>' for i, value in enumerate(input_list)])
        optgroup += f'<optgroup label="{group}" data-selectall="true">{options}</optgroup>'

        html = f'''

            <div class="row p-1">
                <div class="col-4" style="display: grid;">
                    <span>{attribute}</span>
                </div>
                <div class="col-8">
                    <input type="hidden" id="{attribute}" value="{default_option_str}" class="form-control" placeholder="">
                    <select  {input_type}  id="{attribute}_show" name="{attribute}_show" class="" aria-label="{attribute}" onChange="updateExcelCellValue('IN_LINK_DATA', 1, {row}, '{attribute}_show');">
                        {optgroup}
                    </select>
                </div>
            </div>

            '''

    return html



def get_family_input_two_grid(attribute, input_type,default_option_str,row):
    default_option=[]
    engine = create_engine('mysql+mysqlconnector://data_studio:a417528639@156.67.217.3/im_form')
    # cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = 'SELECT * FROM im_form.attribute_setting order by session,sub_session,id'
    attribute_fam = pd.read_sql(query, engine)
    columns = attribute_fam.columns.tolist()
    columns_to_exclude = ['id', 'information_type', 'status', 'enhancement', 'specific_brand', 'linesheet_code', 'field_label', 'field_type', 'both_language', 'description', 'tool_tips', 'session', 'sub_session', 'merge_group', 'sale_channel', 'formula', 'pim_code', 'convertor_function', 'linesheet_code_unit', 'label_desc_en', 'label_desc_th', 'value_desc_format', 'sort_bullet_point', 'grouping_common']
    columns_to_include = [value for value in columns if value not in columns_to_exclude]


    default_option = ["selected" if val in default_option_str.split(",") else "" for val in columns_to_include]

    option = ''.join([f'<option {default_option[i]} value="{value}">{value}</option>' for i,value in enumerate(columns_to_include)])
    #  options = ''.join([f'<option {default_option[i]} value="{value}">{value}</option>' for i, value in enumerate(input_list)])

    html = f'''
        <div class="row p-1">
            <div class="col-4" style="display: grid;">
                <span>{attribute}</span>
            </div>
            <div class="col-8">
                <input disabled type="hidden" id="{attribute}" value="{default_option_str}" class="form-control" placeholder="">
                <select disabled {input_type}  id="{attribute}_show" name="{attribute}_show" class="" aria-label="{attribute}" onChange="updateExcelCellValue('IN_LINK_DATA', 1, '{row}', '{attribute}_show');">
                    {option}
                </select>
            </div>
        </div>
    '''
    return html

def get_single_select_input_cell_by_cell_two_grid(attribute, input_type,default_option_str):
    # default_option_str=''

    default_option=[]
    engine = create_engine('mysql+mysqlconnector://data_studio:a417528639@156.67.217.3/u749625779_cdscontent')
    # cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = f'SELECT input_option FROM u749625779_cdscontent.pim_attr_convert_option_lu where  linesheet_code =  "{attribute}"'
    attribute_option = pd.read_sql(query, engine)
    columns = attribute_option['input_option'].tolist()
    # input_group = np.unique(input_value['option_group'].tolist())

    # default_option = ["selected" if val in default_option_str.split(",") else "" for val in columns]
    default_option = ['selected' if default_option_str == val else '' for val in columns]

    option = ''.join([f'<option {default_option[i]} value="{value}">{value}</option>' for i,value in enumerate(columns)])

    html = f'''
        <div class="row p-1">
            <div class="col-4" style="display: grid;">
                <span>{attribute}</span>
            </div>
            <div class="col-8">
                <input disabled type="hidden" id="{attribute}" value="{default_option_str}" class="form-control" placeholder="">
                <select disabled {input_type}  id="{attribute}_show" name="{attribute}_show" class="" aria-label="{attribute}">
                    {option}
                </select>
            </div>
        </div>
    '''
    return html



# print(get_single_select_input_cell_by_cell_two_grid('gender', 'single',''))

if __name__ == '__main__':
    import sys
    function_name = sys.argv[1]
    args = sys.argv[2:]
    try:
        func = globals()[function_name]
        print(func(*args))
    except KeyError:
        print('Unknown function name:', function_name)
