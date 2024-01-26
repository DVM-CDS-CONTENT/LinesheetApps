import openpyxl
import pandas as pd

import mysql.connector
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import re

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

def process_categories(category_value, row_number, im_form_df, family_template_df):
    category = category_value
    attributes_in_family = ""

    if category:
        print("Processing category:", category)

        attribute_column_index = next((i for i, col in enumerate(family_template_df.columns, start=1) if col == "categories"), 0)

        category_row = family_template_df[family_template_df['categories'] == category]

        missing_attributes = []
        for j in range(2, 8):
            if category_row.empty:
                print(f"Warning on row {row_number}: Category not found in FAMILY_TEMPLATE - {category}")
            else:
                if attribute_column_index > 0:
                    attributes_in_family = category_row.iloc[0, j]

                print("Attributes in FAMILY_TEMPLATE:", attributes_in_family)

                if attributes_in_family:
                    attributes_array = attributes_in_family.split(",")
                    attributes_in_im = [im_form_df.iloc[row_number - 2, im_form_df.columns.get_loc(att)]
                                        for att in attributes_array if att in im_form_df.columns]

                    missing_attributes.extend([att for att in attributes_array if att not in attributes_in_im])

        return row_number, category, missing_attributes

def process_all_rows(im_form_df, family_template_df):

    categories_family_setting_query = convert_gsheets_url('https://docs.google.com/spreadsheets/d/1HbR1_zIgzYyJ-et3QWn40oAVSq8wQipwvttsnlt_Bi0/edit#gid=1850526451')
    categories_family_setting = pd.read_csv(categories_family_setting_query)
    categories_family_setting = categories_family_setting[categories_family_setting['deepen_level']==1]
    categories_family_setting = categories_family_setting[['label_th','family']]
    categories_family_setting = categories_family_setting.fillna("")

    family_setting_query = convert_gsheets_url('https://docs.google.com/spreadsheets/d/1HbR1_zIgzYyJ-et3QWn40oAVSq8wQipwvttsnlt_Bi0/edit#gid=1407377747')
    family_setting = pd.read_csv(family_setting_query)
    # family_setting = attribute_original
    family_setting = family_setting[['linesheet_code' ,'bath_body','fragrance','hair_care','personal_care','health_care','makeup','nails', 'nails_tools','makeup_tools','skincare','gadgets','auto__motorcycle_supplies', 'computers', 'television', 'console_gaming', 'desk_phone', 'mobile__tablets', 'gaming', 'fashion_accessory', 'watches', 'gift_card', 'hampers', 'small_appliances', 'fans__air_purifiers', 'home_equipment__supplies', 'large_appliances', 'tv_accessories', 'home_decoration', 'furniture', 'bedding', 'books', 'hobby', 'cooking_dining', 'grocery', 'stationery', 'pet_equipment__supplies', 'toolings', 'clothing', 'shoes', 'swimwear', 'underwear', 'baby_feeding', 'kids', 'toys', 'sports_accessory', 'sports_equipments', 'camping__equipments', 'luggages', 'travel_accessories']]
    family_setting = family_setting.fillna("")
    family_setting = family_setting.astype(str)




    # Get unique column names (excluding 'linesheet_code')
    try:
        column_names = family_setting.columns[1:]
    except KeyError as err:
        print(err)
    # column_names = family_setting.columns
    # Create a dictionary to store the templates
    templates = {}
    # Iterate over each column name
    for col in column_names:
        template_values = {'R': '', 'O': '', 'N': '', 'AO': '', 'AR': '', "": ''}
        for index, value in enumerate(family_setting[col]):
            template_values[value] += family_setting['linesheet_code'][index] + ','
        templates[col] = template_values
    # Create a new DataFrame for the templates
    templates_df = pd.DataFrame(templates)
    # Reset index and rename index column
    templates_df = templates_df.reset_index().rename(columns={'index': 'family'})
    # Transpose the DataFrame
    templates_df = templates_df.transpose()
    templates_df.columns = templates_df.iloc[0]
    templates_df = templates_df[1:]
    # Reset index and rename index column
    templates_df = templates_df.reset_index().rename(columns={'index': 'family'})
    categories_family_mapping = pd.merge(categories_family_setting, templates_df, on='family', how='left')
    categories_family_mapping.rename(columns={'label_th': 'categories'}, inplace=True)

    for r in dataframe_to_rows(categories_family_mapping, index=False, header=True):
        ws_family_template.append(r)


    category_col_name = "online_categories"  # Replace with the correct column name for "online_categories"
    family_categories_col_name = "categories"

    for selected_row in range(1, im_form_df.shape[0] + 1):
        category_value = im_form_df.loc[selected_row - 1, category_col_name]

        category_warnings = [process_categories(category_value, selected_row, im_form_df, family_template_df)]

        for row_number, category, missing_attributes in category_warnings:
            if missing_attributes:
                print(f"Warning on row {row_number}: Missing attributes in IM_FORM sheet for category {category}: {missing_attributes}")


