import mysql.connector
import pandas as pd
import numpy as np

def get_family():
    cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = 'SELECT * FROM im_form.attribute_setting order by session,sub_session,id'
    attribute = pd.read_sql(query, cnx)
    columns = attribute.columns.tolist()
    columns_to_exclude = ['id', 'information_type', 'linesheet_code', 'field_label', 'field_type', 'both_language', 'session', 'sub_session', 'merge_group', 'sale_channel', 'example_option', 'description', 'formula', 'status', 'specific_brand']
    columns_to_include = [value for value in columns if value not in columns_to_exclude]
    options = ''.join([f'<option value="{value}">{value}</option>' for value in columns_to_include])
    html = f'''
        <label for="stock_source" class="ms-3">Template</label>
        <div class="form-floating m-3">
            <input type="hidden" id="template" name="template" value="">
            <select multiple id="template_show" name="template_show" aria-label="stock_source">
                {options}
            </select>
        </div>
    '''
    return html

def get_input(attribute, type):
    cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    query = f'SELECT * FROM u749625779_cdscontent.job_attribute_option where attribute_table="add_new_job" and attribute_code = "{attribute}"'
    input_value = pd.read_sql(query, cnx)
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
        <label for="stock_source" class="ms-3">{attribute}</label>
        <div class="form-floating m-3">
            <input type="hidden" id="{attribute}" name="{attribute}" value="{default_option_str}">
            <select {type} id="{attribute}_show" name="{attribute}_show" aria-label="{attribute}">
                {optgroup}
            </select>
        </div>
    '''
    return html

if __name__ == '__main__':
    import sys
    function_name = sys.argv[1]
    args = sys.argv[2:]
    try:
        func = globals()[function_name]
        print(func(*args))
    except KeyError:
        print('Unknown function name:', function_name)
