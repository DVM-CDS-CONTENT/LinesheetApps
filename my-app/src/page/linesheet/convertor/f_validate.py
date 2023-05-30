import pandas as pd
import os

path_name = 'my-app/linesheet/CDS_LINESHEET_SANRIO_30_SKUs_TID_20230529180252220.xlsm'
expected_sku_count = 30

def open_file(path_name):
    abs_path = os.path.abspath(path_name)
    sys.stdout.reconfigure(encoding='utf-8')
    df = pd.read_excel(abs_path, skiprows=11)
    actual_sku_count = len(df)
    print(df.head())
    validate_number(actual_sku_count)
    validate_character(df)

def validate_number(actual_sku_count):
    print(actual_sku_count)
    if actual_sku_count == expected_sku_count:
        print("Validation passed: Number of SKUs matches the expected count.")
    else:
        print("Validation failed: Number of SKUs does not match the expected count.")

def validate_character(df):
    for index, row in df.iterrows():
        product_name_th = row['ชื่อสินค้า ภาษาไทย Product Name TH']
        if len(str(product_name_th)) > 100:
            print(f"Validation failed: Product Name TH exceeds 100 characters in row {index+1}: {product_name_th}")

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

if __name__ == '__main__':
    import sys
    open_file(path_name)
