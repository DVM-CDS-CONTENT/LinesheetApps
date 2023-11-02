
from f_function import *
import pandas as pd
import re

def boolean_convertor(linesheet,linesheet_code,my_dict):

    boolean_yes= my_dict['boolean_yes']
    boolean_no= my_dict['boolean_no']
    error= my_dict['error']

    if linesheet[linesheet_code].strip()=='Yes':
        return boolean_yes
    elif linesheet[linesheet_code].strip()=='No':
        return boolean_no
    elif linesheet[linesheet_code].strip()=='':
        return ''
    else:
        error.append("Error:unknown template of boolean in column " +linesheet_code)
        print("Error:unknown template of boolean in column " +linesheet_code + '(def boolean_convertor : f_convert)', flush=True)
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
    if linesheet[linesheet_code] !="":
        mapping_option_value = my_dict['mapping_option_value']
        mapping_option_value=mapping_option_value[mapping_option_value['linesheet_code']==linesheet_code]

        try:
            return mapping_option_value.set_index('input_option')['option_code'][linesheet[linesheet_code]]
        except KeyError:
            # try:
            #     return mapping_option_value.set_index('option_code')['option_code'][linesheet[linesheet_code]]

            # except KeyError as error:
            # print("Warning : "+linesheet_code+" -> "+str(linesheet[linesheet_code]) + " at function simple_select : unable to lookup,used original("+linesheet[linesheet_code]+") instead")

            return linesheet[linesheet_code]
    else:
        return ""


def categories(linesheet, linesheet_code, my_dict):
    categories_mapping = my_dict['categories_mapping']
    # categories_mapping=categories_mapping[categories_mapping['label_th']==linesheet[linesheet_code]]

    try:
        return categories_mapping.set_index('label_en')['full_categories_code'][linesheet[linesheet_code]]
    except KeyError:
        # print(linesheet[linesheet_code])

        return 'unknown categories'+linesheet[linesheet_code] +KeyError

def family(linesheet, linesheet_code, my_dict):

        categories_mapping = my_dict['categories_mapping']
        # categories_mapping = categories_mapping[categories_mapping['label_th']==linesheet[linesheet_code]]

        try:
            return categories_mapping.set_index('label_en')['family'][linesheet['online_categories']]
        except KeyError:
            # print(linesheet[linesheet_code])

            return 'unknown categories'+linesheet['online_categories']


def family_variant(linesheet, linesheet_code, my_dict):

    if linesheet['catalogue_number_for_group'] !='':
        if linesheet['group_by'] !='':
            if linesheet['group_by']=='ไซส์':
                variant = 'size'
            elif linesheet['group_by']=='สี':
                variant = 'color_shade'
            elif linesheet['group_by']=='ไซส์และสี':
                variant = 'size_color_shade'
            elif linesheet['group_by']=='ปริมาณ':
                variant = 'size'

            return str(family(linesheet, 'family', my_dict))+"_"+str(variant)
        else:
            print("Info : group_by is empty", flush=True)
            return ''
    else:
        return ''

def direct_transfer(linesheet,linesheet_code,my_dict):
    value = str(linesheet[linesheet_code])
    try:
        value = float(value)
    except (ValueError, TypeError):
        pass

    return value


def ui_configurable(linesheet,linesheet_code,my_dict):
    boolean_yes= my_dict['boolean_yes']
    boolean_no= my_dict['boolean_no']
    if my_dict[linesheet_code]=='true':
        return boolean_yes
    elif my_dict[linesheet_code]=='false':
        return boolean_no
    else:
        return my_dict[linesheet_code]
    # function_dict = my_dict['function_dict']
    # func  = function_dict[linesheet_code]
    # return func(linesheet,linesheet_code,my_dict)

def shade(linesheet,linesheet_code,my_dict):
    import re
    shade_value = linesheet['color_shade']+'_'+linesheet['color_hex']
    shade_value = re.sub(r'[^\w\s]', '_', shade_value)
    return shade_value

def color_hex(linesheet,linesheet_code,my_dict):

    return linesheet['color_hex']

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
    th_identity_linesheet = my_dict['th_identity_linesheet']
    en_identity_linesheet = my_dict['en_identity_linesheet']
    linesheet_code_with_local =my_dict['linesheet_code_with_local']
    convertor_function = my_dict['convertor_function']

    if '_th' in linesheet_code:
        store=th_identity_linesheet
    else:
        store=en_identity_linesheet


    categories_mapping = my_dict['categories_mapping']
    product_name_append=[]
    i=0
    try:
        product_name_template =  categories_mapping.set_index('label_en')['product_name_template'+store][linesheet['online_categories']]
    except:
        product_name_template =  categories_mapping.set_index('full_categories_code')['product_name_template'+store][linesheet['online_categories']]

    delimiter = "+"
    if product_name_template is not None and product_name_template !='':
        product_name_template_list = product_name_template.split(delimiter)

        for j, attribute in enumerate(product_name_template_list):
            if '"' in attribute:
                product_name_append.append(str(attribute.replace('"', '')))
            else:
                for k, code_with_local in enumerate(linesheet_code_with_local):
                    if code_with_local==attribute and linesheet[attribute] !='' and linesheet[attribute] is not None:
                                if convertor_function[k] == 'simple_select':
                                    if th_identity_linesheet in linesheet_code:
                                        value = lookup_label_option(linesheet, attribute, my_dict, 'option_th', linesheet[attribute])
                                    elif en_identity_linesheet in linesheet_code:
                                        value = lookup_label_option(linesheet, attribute, my_dict, 'option_en',   linesheet[attribute])

                                    if attribute =='size_standard' :
                                        if check_text_or_int(product_name_append[len(product_name_append)-1])!='string':
                                            product_name_append.append(value)
                                    else:
                                            product_name_append.append(value)
                #special color shade
                                elif convertor_function[k] == 'color_shade':
                                    if linesheet['special_shade'+store]=='':
                                        if th_identity_linesheet in linesheet_code:
                                            value = lookup_label_option(linesheet, 'color_shade', my_dict, 'option_th', linesheet['color_shade'])
                                        elif en_identity_linesheet in linesheet_code:
                                            value = lookup_label_option(linesheet, 'color_shade', my_dict, 'option_en',   linesheet['color_shade'])

                                    else:
                                        if th_identity_linesheet in linesheet_code:
                                            value = linesheet['special_shade_th']
                                        elif en_identity_linesheet in linesheet_code:
                                            value = linesheet['special_shade_en']
                                    product_name_append.append(value)
                                else:
                                    if th_identity_linesheet in linesheet_code:
                                        value = str(linesheet[attribute])
                                    elif en_identity_linesheet in linesheet_code:
                                        value = str(linesheet[attribute])
                                    product_name_append.append(value)



            product_name =''.join(map(str, product_name_append))



        # size_value = size_value_template.replace('+','')
    else:
        print('Error : please check'+linesheet['online_categories']+',its missing size template in mapping', flush=True)
        product_name = ''

    #concat get free
    if linesheet['product_sell_type']=='Free Gift':
        if th_identity_linesheet in linesheet_code:
            product_name = '[ของแถม]'+product_name
        elif en_identity_linesheet in linesheet_code:
            product_name = '[GET FREE]'+product_name


    return product_name
def content_note(linesheet,linesheet_code,my_dict):
    from datetime import date
    today = date.today()
    return "Generate template from convertor (New IM-FORM) at "+str(today)

def is_set(linesheet,linesheet_code,my_dict):
    boolean_yes= my_dict['boolean_yes']
    boolean_no= my_dict['boolean_no']
    error= my_dict['error']
    if linesheet['set_include']!='':
        return boolean_yes
    else:
        return boolean_no


def description(linesheet, linesheet_code, my_dict):
    # Define variables
    th_identity_linesheet = my_dict['th_identity_linesheet']
    en_identity_linesheet = my_dict['en_identity_linesheet']
    label_desc_th = my_dict['label_desc_th']
    label_desc_en = my_dict['label_desc_en']
    linesheet_code_with_local = my_dict['linesheet_code_with_local']
    linesheet_columns = my_dict['linesheet_columns']
    ms_delimiter = my_dict['ms_delimiter']
    convertor_function = my_dict['convertor_function']
    caution_th = my_dict['caution_th']
    caution_en = my_dict['caution_en']
    bullet = ""
    label = ""

    new_value_list = []
    linesheet_code_unit = my_dict['linesheet_code_unit']
    configurable_ao_family=my_dict['configurable']

    family_template = family(linesheet, 'online_categories', my_dict)

    configurable_ao_family_set = configurable_ao_family[family_template].values.tolist()

    # Generate bullet point
    for i, code_with_local in enumerate(linesheet_code_with_local):
        value=''
        label=''
        if code_with_local in linesheet:
        # if 1==1:
            if configurable_ao_family_set[i]!='AO' and configurable_ao_family_set[i]!='AR' and configurable_ao_family_set[i]!='N':
                if (label_desc_en[i] != "-" and label_desc_en[i] != "" and linesheet[code_with_local] != '' and label_desc_en[i]):
                    # Translate options in case of simple select
                    if convertor_function[i] == 'simple_select':
                        if th_identity_linesheet in linesheet_code:
                            label = label_desc_th[i]
                            value = lookup_label_option(linesheet, code_with_local, my_dict, 'option_th',linesheet[code_with_local])
                        elif en_identity_linesheet in linesheet_code:
                            label = label_desc_en[i]
                            value = lookup_label_option(linesheet, code_with_local, my_dict, 'option_en',linesheet[code_with_local])
                    # Translate options in case of multi-select
                    elif convertor_function[i] == 'multi_select_option':
                        value_list = linesheet[code_with_local].split(ms_delimiter)
                        for value in value_list:
                            value = value.strip()
                            if th_identity_linesheet in linesheet_code:
                                new_value = lookup_label_option(linesheet, code_with_local, my_dict, 'option_th', value)
                                new_value_list.append(new_value)
                            elif en_identity_linesheet in linesheet_code:
                                new_value = lookup_label_option(linesheet, code_with_local, my_dict, 'option_en', value)
                                new_value_list.append(new_value)

                        if th_identity_linesheet in linesheet_code:
                            label = label_desc_th[i]
                        elif en_identity_linesheet in linesheet_code:
                            label = label_desc_en[i]

                        value = ms_delimiter.join(new_value_list)


                    # Boolean convertor
                    elif convertor_function[i] == 'boolean_convertor':
                        if th_identity_linesheet in linesheet_code:
                            if linesheet[code_with_local].lower() == 'yes':
                                label = label_desc_th[i]
                                value = 'ใช่'
                            elif th_identity_linesheet in linesheet_code:
                                value = ''
                        if en_identity_linesheet in linesheet_code:
                            if linesheet[code_with_local].lower() == 'yes':
                                label = label_desc_en[i]
                                value = 'Yes'
                            elif th_identity_linesheet in linesheet_code:
                                value = ''

                    #special color shade
                    elif convertor_function[i] == 'color_shade':
                        if linesheet['special_shade_en']=='':
                            if th_identity_linesheet in linesheet_code:
                                label = label_desc_th[i]
                                value = lookup_label_option(linesheet,'color_shade', my_dict, 'option_th', linesheet['color_shade'])
                            elif en_identity_linesheet in linesheet_code:
                                label = label_desc_en[i]
                                value = lookup_label_option(linesheet,'color_shade', my_dict, 'option_en', linesheet['color_shade'])
                        else:
                            if th_identity_linesheet in linesheet_code:
                                label = label_desc_th[i]
                                value = linesheet['special_shade_th']
                            elif en_identity_linesheet in linesheet_code:
                                label = label_desc_en[i]
                                value = linesheet['special_shade_en']

                    # Translate options in case of unidentified
                    else:
                        if th_identity_linesheet in linesheet_code:
                            label = label_desc_th[i]
                            value = str(linesheet[code_with_local])
                        elif en_identity_linesheet in linesheet_code:
                            label = label_desc_en[i]
                            value = str(linesheet[code_with_local])

                    # Translate unit of value
                    try:
                        if check_text_or_int(linesheet[code_with_local])!='string':
                            if linesheet_code_unit[i] and linesheet_code_unit[i] != '' and linesheet[linesheet_code_unit[i]] != '':
                                if th_identity_linesheet in linesheet_code:
                                    unit = lookup_label_option(linesheet, linesheet_code_unit[i], my_dict, 'option_th',
                                                            linesheet[linesheet_code_unit[i]])
                                elif en_identity_linesheet in linesheet_code:
                                    unit = lookup_label_option(linesheet, linesheet_code_unit[i], my_dict, 'option_en',
                                                            linesheet[linesheet_code_unit[i]])
                                value = str(value) + ' ' + str(unit)
                            else:
                                unit = ''
                                value = value
                    except :
                        print('Warning: '+linesheet_code_unit[i]+' is not defined for ', flush=True)


                    try:
                        if str(label) !='' and str(value) !='':
                            bullet += '<li>' + str(label) + ' : ' + str(value) + '</li>\n'
                    except :
                        print('Error: label is not defined for ' + code_with_local, flush=True)

                    new_value_list = []




    # Add set include
    if 'set_include' in linesheet.index:
        set_include=linesheet['set_include']
    else:
        set_include=''
    set_includes_html = convert_to_html_with_li(set_include)
    set_includes_path = '_set_include' if set_include else ''

    # Selected layout
    categories_mapping = my_dict['categories_mapping']
    layout_name = categories_mapping.set_index('label_en')['description_block_template'][linesheet['online_categories']]
    layout_th = 'description_layout\\th\\' + layout_name + set_includes_path + '_th.html'
    layout_en = 'description_layout\\en\\' + layout_name + set_includes_path + '_en.html'

    # Replace with template
    if th_identity_linesheet in linesheet_code:
        description = get_html_value(layout_th, 'div', {'id': 'my-div'})
        description = description.replace("#product_name", linesheet['product_name_th'])

        description = description.replace("#bullet_point", bullet)
        description = description.replace("#short_description", linesheet['short_description_th'])
        description = description.replace("#product_information", markdown_to_html(linesheet['product_information_th']))
        description = description.replace("#set_include", set_includes_html)
        description = description.replace("#caution", caution_th)
    elif en_identity_linesheet in linesheet_code:
        description = get_html_value(layout_en, 'div', {'id': 'my-div'})
        description = description.replace("#product_name", linesheet['product_name_en'])

        description = description.replace("#bullet_point", bullet)
        description = description.replace("#short_description", linesheet['short_description_en'])
        description = description.replace("#product_information",  markdown_to_html(linesheet['product_information_en']))
        description = description.replace("#set_include", set_includes_html)
        description = description.replace("#caution", caution_en)

    return description


def default_dimension(linesheet,linesheet_code,my_dict):
    if linesheet_code in linesheet:
        if linesheet[linesheet_code] != '':
            return linesheet[linesheet_code]
        else:
            return 1
    else:
        return 1

def default_unit_dimension(linesheet,linesheet_code,my_dict):
    if linesheet_code in linesheet:
        if linesheet[linesheet_code] != '':
            option_code =  simple_select(linesheet, linesheet_code, my_dict)
            return option_code
        else:
            return 'cm'
    else:
        return 'cm'

def default_package_dimension(linesheet,linesheet_code,my_dict):
    if linesheet_code in linesheet:
        if linesheet[linesheet_code] != '':
            option_code =  simple_select(linesheet, linesheet_code, my_dict)
            return option_code
        else:
            return '14_5_x_21_5_x_7_5_cm_'
    else:
        return '14_5_x_21_5_x_7_5_cm_'

def bu(linesheet,linesheet_code,my_dict):
    if linesheet['brand_name'].lower() == 'muji':
        return 'MJT'
    else:
        return 'CDS'

def min_qty(linesheet,linesheet_code,my_dict):
    return 1

def use_config_min_qty(linesheet,linesheet_code,my_dict):
    return  my_dict['boolean_yes']

def payment_methods(linesheet,linesheet_code,my_dict):
    price = int(linesheet['original_price_in_vat'])
    if price==None:
        price=0

    if price>=7000:
            payment_value = "payment_service_bank_transfer,payment_service_fullpayment"
    else:
            payment_value = "payment_service_bank_transfer,payment_service_fullpayment,cashondelivery,payatstore"

    if my_dict['allow_installment']=='true':
            payment_value +="payment_service_installment"

    return payment_value

def shipping_methods(linesheet,linesheet_code,my_dict):
    try:
        shipping_methods=str()

        package_dimension = default_package_dimension(linesheet,linesheet_code,my_dict)
        if linesheet['product_sell_type']=='Pre-order':
            shipping_methods='cds_standard,pickupatstore_pickupatstore'
        elif linesheet['product_sell_type']=='Normal' or linesheet['product_sell_type']=='Free Gift':
            shipping_methods='cds_standard'

        if linesheet['one_hr_pickup']=='Yes' or linesheet['brand_name'] in my_dict['shipping_mapping_one_hr']:
            shipping_methods+=',storepickup_ispu'

        if (linesheet['one_hr_pickup']=='Yes' or linesheet['brand_name'] in my_dict['shipping_mapping_one_hr']) and package_dimension != '40_x_45_x_35_cm_' and package_dimension != "special_size" :
            shipping_methods+=',grab_ship_from_store'

        if allow_cc(linesheet,linesheet_code,my_dict) == 1 and linesheet['product_sell_type']!='Pre-order':
            shipping_methods+=',pickupatstore_pickupatstore'
    except KeyError as error:
        return 'Error : shipping_methods function : '+str(error)


    return shipping_methods

def size(linesheet,linesheet_code,my_dict):
    categories_mapping = my_dict['categories_mapping']
    convertor_function = my_dict['convertor_function']
    linesheet_code_with_local = my_dict['linesheet_code_with_local']
    size_value=''
    size_template=[]
    size_value_lookup=''
    i=0
    try:
        size_value_template  =  categories_mapping.set_index('label_en')['size_value_template'][linesheet['online_categories']]
    except:
        size_value_template  =  categories_mapping.set_index('full_categories_code')['size_value_template'][linesheet['online_categories']]

    delimiter = "+"
    if size_value_template is not None:
        size_value_template_list = size_value_template.split(delimiter)

        if check_text_or_int(linesheet[size_value_template_list[0]])=='string':
            size_value = linesheet[size_value_template_list[0]]
            size_template.append(size_value_lookup)
        else:
            for j, attribute in enumerate(size_value_template_list):
                if i < 2:
                    if linesheet[attribute]!='':
                        i+=1
                        for k, code_with_local in enumerate(linesheet_code_with_local):
                            if code_with_local==attribute :
                                if convertor_function[k] == 'simple_select':
                                    size_value_lookup = lookup_label_option(linesheet, attribute, my_dict, 'option_code',linesheet[attribute])
                                    size_template.append(size_value_lookup)
                                else:
                                    size_value_lookup = linesheet[attribute]
                                    size_template.append(size_value_lookup)

            size_value ='_'.join(map(str, size_template))
            # size_value = re.sub(r"[^a-zA-Z0-9 ]", "_", size_value)

        # size_value = size_value_template.replace('+','')
    else:
        print('Warning : please check'+str(linesheet['online_categories'])+',its missing size template in mapping', flush=True)
        size_value = ''

    return size_value


def brand_name(linesheet,linesheet_code,my_dict):
    mapping_option_value = my_dict['mapping_option_value']
    mapping_option_value=mapping_option_value[mapping_option_value['linesheet_code']==linesheet_code]

    try:
        return mapping_option_value.set_index('input_option')['option_code'][linesheet[linesheet_code]]
    except KeyError:
        try:
            brand_name = re.sub(r"[^a-zA-Z0-9 ]", "_", linesheet[linesheet_code])
            return brand_name
        except KeyError as error:
            print('Error : brand name error ->'+str(KeyError), flush=True)
            return 'Error at function brand_name :'+str(error)


def max_qty_per_order(linesheet,linesheet_code,my_dict):
    return 10

def manual_update_attributes(linesheet,linesheet_code,my_dict):
    return 'size,color_shade,manual_grouping,name,catalog_no'

def special_color_shade(linesheet,linesheet_code,my_dict):
    return ''


def color_shade(linesheet,linesheet_code,my_dict):
    mapping_option_value = my_dict['mapping_option_value']
    mapping_option_value=mapping_option_value[mapping_option_value['linesheet_code']==linesheet_code]
    if linesheet['special_shade_en']=='':
        value =  mapping_option_value.set_index('input_option')['option_code'][linesheet['color_shade']]
    else:
        value = linesheet['ibc']+'_'+linesheet['special_shade_en']
        value = re.sub(r"[^a-zA-Z0-9 ]", "_", value)

    return value


def common_name(linesheet,linesheet_code,my_dict):
    return linesheet[linesheet_code]


def color_group(linesheet,linesheet_code,my_dict):
    color_mapping = my_dict['color_mapping']
    try:
        value =  color_mapping.set_index('input_option')['color_group_pim_code'][linesheet['color_shade']]
    except:
        value =  color_mapping.set_index('option_code')['color_group_pim_code'][linesheet['color_shade']]
    return value

def allow_cod(linesheet,linesheet_code,my_dict):
    price = int(linesheet['original_price_in_vat'])
    if price==None:
        price=0
    if int(linesheet['original_price_in_vat'])<7000:
        return 1
    else:
        return 0

def allow_cc(linesheet,linesheet_code,my_dict):
    price = int(linesheet['original_price_in_vat'])
    if price==None:
        price=0
    if int(linesheet['original_price_in_vat'])<7000:
        return 1
    else:
        return 0

def allow_gift_wrapping(linesheet,linesheet_code,my_dict):
    price = int(linesheet['original_price_in_vat'])
    if price==None:
        price=0
    if int(linesheet['original_price_in_vat'])>200 :
        return 1
    else:
        return 0

def group_name(linesheet,linesheet_code,my_dict):
    original_linesheet = my_dict['original_linesheet']
    return original_linesheet['product_name_en']

def product_status(linesheet,linesheet_code,my_dict):
    return 'Normally'



























