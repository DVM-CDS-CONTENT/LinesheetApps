from bs4 import BeautifulSoup
import os
import importlib
import re
import markdown

def format_number(number):
    try:
        number_float = float(number)
        if number_float.is_integer():
            return str(int(number_float))
        else:
            return str(number_float)
    except ValueError:
        return number  # Handle non-convertible values as-is

def get_html_value(html_file, tag, attribute=None):
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    # Load HTML file

    with open(current_directory+html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    # with open(parent_directory+'\\spear\\resources\\src\\page\\linesheet\\convertor\\'+html_file, 'r', encoding='utf-8') as f:
    #     html = f.read()

    return html

def removesuffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text

def lookup_label_option(linesheet, code_with_local, my_dict , language,value):

    value = format_number(value)

    try:
        mapping_option_value = my_dict['mapping_option_value']
        mapping_option_value = mapping_option_value[mapping_option_value['linesheet_code']==code_with_local]

        label = mapping_option_value.set_index('input_option')[language][value]
    except KeyError as err:
        try:
            # print('Error : '+str(code_with_local)+' : '+ str(err), flush=True)
            mapping_option_value = my_dict['mapping_option_value']
            mapping_option_value = mapping_option_value[mapping_option_value['linesheet_code']==code_with_local]
            label = mapping_option_value.set_index('option_code')[language][value]
        except KeyError as error:
            print('Error at function lookup_label_option : '+str(code_with_local)+' : '+ str(error), flush=True)
            label='Error : '+str(code_with_local)+' : '+ str(error)
    return label


# def add_parent_column(df, parent_prefix, parent_bu, parent_pa_id, parent_year, parent_month,running):
#     import pandas as pd

#     # try:
#         # create a dictionary that maps each catalog to a group number
#     catalog_groups = {}
#     for catalog in df['catalogue_number_for_group'].unique():
#         if len(df[df['catalogue_number_for_group'] == catalog]) > 1 :
#             parent_running = str(running).zfill(4)
#             parent_month = str(parent_month).zfill(2)
#             parent_year = str(parent_year).zfill(2)
#             parent_id = f'{parent_prefix}{parent_bu}{parent_pa_id}{parent_year}{parent_month}{parent_running}'
#             catalog_groups[catalog] = f'{parent_id}'
#             running += 1
#         else:
#             catalog_groups[catalog] = ''

def add_parent_column(df, parent_prefix, parent_bu, parent_pa_id, parent_year, parent_month, running):
    import pandas as pd

    try:
        # Create a dictionary that maps each catalog to a group number
        catalog_groups = {}
        for catalog in df['catalogue_number_for_group'].unique():
            if len(df[df['catalogue_number_for_group'] == catalog]) > 1:
                parent_running = str(running).zfill(4)
                parent_month = str(parent_month).zfill(2)
                parent_year = str(parent_year).zfill(2)
                parent_id = f'{parent_prefix}{parent_bu}{parent_pa_id}{parent_year}{parent_month}{parent_running}'
                catalog_groups[catalog] = f'{parent_id}'
                running += 1
            else:
                catalog_groups[catalog] = ''

        # Create a new DataFrame with the 'parent' column
        parent_series = pd.Series([catalog_groups[catalog] for catalog in df['catalogue_number_for_group']], name='parent')
        new_columns = pd.concat([df, parent_series], axis=1)

        # Update the 'parent' column for rows with an empty 'catalogue_number_for_group'
        new_columns.loc[new_columns['catalogue_number_for_group'] == '', 'parent'] = ''
    except KeyError as error:
        print('Error: group error -> ' + str(df.columns), flush=True)
        return df

    return new_columns

# Example usage:
# df = add_parent_column(df, 'prefix', 'bu', 'pa_id', 'year', 'month', 1)



#     # add the group column to the dataframe
#     df['parent'] = [catalog_groups[catalog] for catalog in df['catalogue_number_for_group']]
#     df.loc[(df['catalogue_number_for_group'] == ''), 'parent'] = ''
#     # except KeyError as error:
#     #     print('Error : group error ->'+str(df.columns), flush=True)

#     return df



def remove_empty_columns(df):
    # Get boolean mask of columns that have at least one non-null value
    non_empty_cols = df.notnull().any(axis=0)
    # Get boolean mask of columns that have at least one non-blank value
    non_blank_cols = df.apply(lambda x: x.str.strip().astype(bool)).any(axis=0)
    # Combine the two masks to get columns that have at least one non-null and non-blank value
    non_empty_blank_cols = non_empty_cols & non_blank_cols
    # Get the list of empty columns
    empty_cols = df.columns[~non_empty_blank_cols].tolist()
    # Drop the empty columns from the DataFrame
    df = df.drop(empty_cols, axis=1)
    # Return the modified DataFrame
    return df

def rename_parent_column_and_move_positioning(df):
    # rename the 'B' column to 'new_column_name'
    df = df.rename(columns={'parent': 'code'})


    # move the 'new_column_name' column to the beginning of the dataframe
    cols = list(df.columns)
    cols.insert(0, cols.pop(cols.index('code')))
    df = df[cols]
    return df

def move_positioning_template(df):

    # move the 'new_column_name' column to the beginning of the dataframe
    cols = list(df.columns)
    cols.insert(1, cols.pop(cols.index('parent')))
    df = df[cols]
    return df

def remove_excel_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def function_exists(module_name, function_name):
    try:
        module = importlib.import_module(module_name)
        return hasattr(module, function_name) and callable(getattr(module, function_name))
    except ImportError:
        return False

def convert_to_html_with_li(text):
    items = text.split('\n')
    html = '<ul>\n'
    for item in items:
        if item.strip() != '':
            html += f'<li>{item.strip()}</li>\n'
    html += '</ul>'
    return html



def check_text_or_int(value):
    if isinstance(value, int):
        return "Integer"
    elif isinstance(value, str):
        if re.match(r'^-?\d+(\.\d+)?$', value):
            return "Integer"
        return "string"
    else:
        return "Neither text nor integer"



def markdown_to_html(markdown_text):
    html_output = markdown.markdown(markdown_text)
    return html_output

def replace_column_values_with_lookup(input_df, lookup_df, input_column, input_primary_key, lookup_primary_key , column_get):
    lookup_dict = dict(zip(lookup_df[lookup_primary_key], lookup_df[column_get]))
    input_df[input_column] = input_df[input_primary_key].map(lookup_dict)
    return input_df





















