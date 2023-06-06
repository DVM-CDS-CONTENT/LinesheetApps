import pandas as pd
import os

path_name = 'my-app/linesheet/CDS_LINESHEET_SANRIO_30_SKUs_TID_20230529180252220.xlsm'
expected_sku_count = 30
expected_types = ['.xlsm','.xlsx']


def open_file(path_name):
    abs_path = os.path.abspath(path_name)
    sys.stdout.reconfigure(encoding='utf-8')
    df = pd.read_excel(abs_path, skiprows=11)
    actual_sku_count = len(df)
    # print(df.head())
    validate_number(actual_sku_count)
    validate_character_th(df)
    validate_type(path_name, expected_types)

def validate_number(actual_sku_count):
    # print(actual_sku_count)
    if actual_sku_count == expected_sku_count:
        print("Validation passed: Number of SKUs matches the expected count.")
    else:
        print("Validation failed: Number of SKUs does not match the expected count.")

def validate_character_th(df):
    count_correct = 0
    count_notcorrect = 0
    product_name_th_error = []
    
    for _, row in df.iterrows():
        product_name_th = row['ชื่อสินค้า\nProduct Name [Thai]']
        ibc_no = row['IBC No.']
        try:
            if len(product_name_th) < 20:
                count_correct += 1
            else:
                count_notcorrect += 1
                product_name_th_error.append((str(ibc_no),product_name_th))
        except TypeError:
            pass
    
    print(f"Correct count: {count_correct}")
    print(f"Not correct count: {count_notcorrect}")

    if len(product_name_th_error) > 0:
        print("CDS with characters exceeding 20:")
        for _, name in product_name_th_error:
            print(f"CDS{_}: {name}")
    else:
        print(True)
    validate_character_en(df)

def validate_character_en(df):
    count_correct = 0
    count_notcorrect = 0
    product_name_en_error = []
    
    for _, row in df.iterrows():
        product_name_en = row['ชื่อสินค้า\nProduct Name [English]']
        ibc_no = row['IBC No.']
        try:
            if len(product_name_en) < 20:
                count_correct += 1
            else:
                count_notcorrect += 1
                product_name_en_error.append((str(ibc_no),product_name_en))
        except TypeError:
            pass
    
    print(f"Correct count: {count_correct}")
    print(f"Not correct count: {count_notcorrect}")

    if len(product_name_en_error) > 0:
        print("CDS with characters exceeding 20:")
        for _, name in product_name_en_error:
            print(f"CDS{_}: {name}")
    else:
        print(True)

def validate_type(file_path, expected_type):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension.lower() in [ext.lower() for ext in expected_types]:
        print("File type is valid.")
    else:
        print("File type is not valid.")

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
