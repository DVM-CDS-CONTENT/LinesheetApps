def get_family():
        import mysql.connector
        import pandas as pd
        # Connect to the database
        cnx = mysql.connector.connect(user='data_studio', password='a417528639', host='156.67.217.3', database='im_form')
        # Execute a SELECT statement and read the results into a Pandas DataFrame
        query = 'SELECT * FROM im_form.attribute_setting order by session,sub_session,id'
        attribute = pd.read_sql(query, cnx)
        columns = attribute.columns.tolist()
        option = ''
        # revise the list to HTML option
        for i, value in enumerate(columns):
                if value not in(
                        'id',
                        'information_type',
                        'linesheet_code',
                        'field_label',
                        'field_type',
                        'both_language',
                        'session',
                        'sub_session',
                        'merge_group',
                        'sale_channel',
                        'example_option',
                        'description',
                        'formula',
                        'status',
                        'specific_brand'
                ):
                        option += '<option value="'+value+'" >'+value+'</option>'
        html = '''
        <label for="stock_source" class="ms-3">Template</label>
        <div class="form-floating m-3">
        <input type="hidden" id="template" name="template" value="">
                <select multiple  id="template_show" name="template_show" aria-label="stock_source">
                '''+ option +'''
                </select>
        </div>
                '''
        return html

x = get_family()
print(x)
