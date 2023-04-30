
import tkinter
import tkinter.messagebox
import openpyxl
import mysql.connector
import pandas as pd
import eel
from random import randint



@app.route('/get_input', methods=['POST'])
def get_input(attribute,type):
    import mysql.connector
    import pandas as pd
    import numpy as np
    # Connect to the database
    cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
    # Execute a SELECT statement and read the results into a Pandas DataFrame
    query = 'SELECT * FROM u749625779_cdscontent.job_attribute_option where attribute_table="add_new_job" and attribute_code = "'+attribute+'"'
    input_value = pd.read_sql(query, cnx)
    print(input_value['option_group'])
    input_value['option_group'] = input_value['option_group'].fillna(input_value['attribute_code'])
    input_group = input_value['option_group'].tolist()
    input_group = np.unique(input_group)
    optgroup =""
    for j, group in enumerate(input_group):
        input_value_filter = input_value[input_value['option_group']==group]
        input_list = input_value_filter['attribute_option_code'].tolist()
        default_option = input_value_filter['default_option'].tolist()
        default_option_list = []
        optgroup +='''<optgroup label="'''+group+'''" data-selectall="true">'''
        option =''
        for i, value in enumerate(input_list):
            default_option[i] = default_option[i].replace("yes", "selected")
            default_option[i] = default_option[i].replace("no", "")
            if  default_option[i]=='yes':
                default_option_list.append(value)
            option += '<option '+default_option[i]+' value="'+value+'">'+value+'</option>'
        default_option_str= ",".join(default_option_list)
        optgroup +=  option
        optgroup += ''' </optgroup>'''

    html = '''
          <label for="stock_source" class="ms-3">'''+attribute+'''</label>
            <div class="form-floating m-3">
            <input type="hidden" id="'''+attribute+'''" name="'''+attribute+'''" value="'''+default_option_str+'''">
                    <select '''+type+'''   id="'''+attribute+'''_show" name="'''+attribute+'''_show" aria-label="'''+attribute+'''">
                        '''+optgroup+'''
                    </select>
            </div>
        '''
    return html






if __name__ == '__main__':
    app.run()




