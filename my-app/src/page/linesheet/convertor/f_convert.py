
from f_function import *
import pandas as pd

def boolean_convertor(linesheet,linesheet_code,my_dict):

    boolean_yes= my_dict['boolean_yes']
    boolean_no= my_dict['boolean_no']
    error= my_dict['error']

    if linesheet[linesheet_code]=='Yes':
        return boolean_yes
    elif linesheet[linesheet_code]=='No':
        return boolean_no
    else:
        error.append("error:unknown template of boolean in column " +linesheet_code)
        return "error:unknown template of boolean " +linesheet_code

def multi_select_option(linesheet, linesheet_code, my_dict):
    mapping_option_value = my_dict['mapping_option_value']
    mapping_option_value=mapping_option_value[mapping_option_value['linesheet_code']==linesheet_code]
    ms_delimiter=my_dict['ms_delimiter']

    new_value_list =[]
    if linesheet[linesheet_code]!="":
        value_list = linesheet[linesheet_code].split(ms_delimiter)
        for value in value_list:
            try:
                return mapping_option_value.set_index('input_option')['option_code'][value]
            except KeyError:
                return value

def simple_select(linesheet, linesheet_code, my_dict):
    mapping_option_value = my_dict['mapping_option_value']
    mapping_option_value=mapping_option_value[mapping_option_value['linesheet_code']==linesheet_code]

    try:
        return mapping_option_value.set_index('input_option')['option_code'][linesheet[linesheet_code]]
    except KeyError:
        return linesheet[linesheet_code]

def direct_transfer(linesheet,linesheet_code,my_dict):

    return linesheet[linesheet_code]

def shade(linesheet,linesheet_code,my_dict):
    import re
    shade_value = linesheet['color_shade']+'_'+linesheet['color_hex']
    shade_value = re.sub(r'[^\w\s]', '_', shade_value)
    return shade_value

def sku(linesheet,linesheet_code,my_dict):
    try:
        if linesheet['brand_name'] == 'MUJI':
            sku = 'MJT'+linesheet['ibc']
        else:
            sku = 'CDS'+linesheet['ibc']
    except:
        sku = 'CDS'+linesheet['ibc']
    return sku

def product_name(linesheet,linesheet_code,my_dict):
    return linesheet[linesheet_code]

def content_note(linesheet,linesheet_code,my_dict):
    from datetime import date
    today = date.today()
    return "Generate template from convertor (New IM-FORM) at "+today

def description(linesheet,linesheet_code,my_dict):

#define var

    th_identity_linesheet = my_dict['th_identity_linesheet']
    en_identity_linesheet = my_dict['en_identity_linesheet']
    label_desc_th = my_dict['label_desc_th']
    label_desc_en = my_dict['label_desc_en']
    linesheet_code_with_local = my_dict['linesheet_code_with_local']
    linesheet_columns=my_dict['linesheet_columns']

    ms_delimiter=my_dict['ms_delimiter']
    convertor_function=my_dict['convertor_function']
    caution_th=my_dict['caution_th']
    caution_en=my_dict['caution_en']
    bullet=""
    new_value_list =[]


#generate bullet point

#todo:
#_____1.add unit of attribute
#_____2.translate simple select value-done, Done
#_____3.translate multi select value, Done

    for i , code_with_local in enumerate(linesheet_code_with_local):
        if code_with_local in linesheet_columns:
                #check value available to insert in description
                if(label_desc_en[i] and label_desc_en[i] != "-" and linesheet[code_with_local]):
                    ## translate options incase simple select
                    if convertor_function[i]=='simple_select':
                        if th_identity_linesheet in linesheet_code:
                            label= label_desc_th[i]
                            value = lookup_label_option(linesheet, code_with_local, my_dict , 'option_th')
                        elif en_identity_linesheet in linesheet_code:
                            label= label_desc_en[i]
                            value = lookup_label_option(linesheet, code_with_local, my_dict , 'option_en')
                    ## translate options incase multi select
                    elif convertor_function[i]=='multi_select_option':

                        value_list = linesheet[code_with_local].split(ms_delimiter)
                        for value in value_list:
                            value = value.strip()
                            if th_identity_linesheet in linesheet_code:
                                new_value = lookup_label_option(linesheet, code_with_local, my_dict , 'option_th')
                                new_value_list.append(new_value)
                            elif en_identity_linesheet in linesheet_code:
                                new_value = lookup_label_option(linesheet, code_with_local, my_dict , 'option_en')
                                new_value_list.append(new_value)
                        if th_identity_linesheet in linesheet_code:
                            label= label_desc_th[i]
                        elif en_identity_linesheet in linesheet_code:
                            label= label_desc_en[i]

                        value = ms_delimiter.join(new_value_list)

                    ## translate options incase unidentified
                    else:
                        if th_identity_linesheet in linesheet_code:
                            label= label_desc_th[i]
                            value = str(linesheet[code_with_local])
                        elif en_identity_linesheet in linesheet_code:
                            label= label_desc_en[i]
                            value = str(linesheet[code_with_local])
                        ## insert the value in to description

                    bullet += '<li>'+label+' : '+value+'</li>'

# Replace with template

    if th_identity_linesheet in linesheet_code:
        description = get_html_value('my-app/src/page/linesheet/convertor/description_layout/block_general.html', 'div', {'id': 'my-div'})
        description = description.replace("#bullet_point", bullet)
        description = description.replace("#short_description", linesheet['description_th'])
        description = description.replace("#caution", caution_th)
    elif en_identity_linesheet in linesheet_code:
        description = get_html_value('my-app/src/page/linesheet/convertor/description_layout/block_general.html', 'div', {'id': 'my-div'})
        description = description.replace("#bullet_point", bullet)
        description = description.replace("#short_description", linesheet['description_en'])
        description = description.replace("#caution", caution_en)


    return description











