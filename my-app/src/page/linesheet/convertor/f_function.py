from bs4 import BeautifulSoup

def get_html_value(html_file, tag, attribute=None):
    # Load HTML file
    with open(html_file, 'r') as f:
        html = f.read()

    return html

def removesuffix(text, suffix):
    if text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text

def lookup_label_option(linesheet, code_with_local, my_dict , language):
    mapping_option_value = my_dict['mapping_option_value']
    warning = my_dict['warning']
    info = my_dict['info']
    mapping_option_value = mapping_option_value[mapping_option_value['linesheet_code']==code_with_local]


    return mapping_option_value.set_index('input_option')[language][linesheet[code_with_local]]


def add_parent_column(df, parent_prefix, parent_bu, parent_pa_id, parent_year, parent_month,running):
    import pandas as pd

    # create a dictionary that maps each catalog to a group number
    catalog_groups = {}
    for catalog in df['catalogue_number_for_group'].unique():
        if len(df[df['catalogue_number_for_group'] == catalog]) > 1:
            parent_running = str(running).zfill(4)
            parent_id = f'{parent_prefix}{parent_bu}{parent_pa_id}{parent_year}{parent_month}{parent_running}'
            catalog_groups[catalog] = f'{parent_id}'
            running += 1
        else:
            catalog_groups[catalog] = ''

    # add the group column to the dataframe
    df['parent'] = [catalog_groups[catalog] for catalog in df['catalogue_number_for_group']]
    return df



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













