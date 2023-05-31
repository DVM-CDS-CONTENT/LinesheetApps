import pandas as pd
import os
import sys


expected_sku_count = 30


def open_file(path_name):
    abs_path = os.path.abspath(path_name)
    sys.stdout.reconfigure(encoding='utf-8')
    df = pd.read_excel(abs_path, skiprows=11)
    actual_sku_count = len(df)
    print(df.to_string())

    validate_number(actual_sku_count)
    validate_character_th(df)

def validate_number(actual_sku_count):
    # print(actual_sku_count)
    if actual_sku_count == expected_sku_count:
        result_sku = "validate number of sku equal with count of sku in Linesheet."
    else:
        result_sku = "validate number of sku not equal with count of sku in Linesheet."
    print(result_sku)

def validate_character_th(df):
    count_correct = 0
    count_notcorrect = 0
    product_name_th_error = []
    for index, row in df.iterrows():
        product_name_th = row['ชื่อสินค้า\nProduct Name [Thai]']
        try:
            if len(product_name_th) < 20:
                # print(len(product_name_th))
                count_correct = count_correct+1
            else:
                count_notcorrect = count_notcorrect + 1
                product_name_th_error.append(product_name_th)
                # print(len(product_name_th),product_name_th)

        except TypeError:
        # Handle the case where product_name_th is not a string
            print("Invalid value for product name")
    print(count_correct)
    print(count_notcorrect)
    print(product_name_th_error)


def validate_size(df):
    pass

def validate_dropdown(df):
    pass

def validate_productname_en(df):
    pass

def validate_productname_th(df):
    pass

def validate_category(df):
    pass

if __name__ == 'main':

    path_name = sys.argv[1]
    open_file(path_name)
