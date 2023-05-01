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



