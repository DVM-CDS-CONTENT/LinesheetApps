import os
from datetime import datetime


if __name__ == '__main__':
    import sys
    folder_name = sys.argv[1]

# Your current directory (including python script & all excel files)
mydir = (os.getcwd()).replace('\\','/') + '/'

# Get all Excel files in the 'linesheet' folder with their creation and update dates
excel_files = []
for path, subdirs, files in os.walk(mydir):
    if folder_name in path:
        for file in files:
            if file.endswith('.xlsx') or file.endswith('.xlsm') or file.endswith('.XLS'):
                file_path = os.path.join(path, file)
                creation_time = os.path.getctime(file_path)
                update_time = os.path.getmtime(file_path)
                excel_files.append((file, creation_time, update_time))

# Sort the Excel files by creation date in descending order
excel_files.sort(key=lambda x: x[1], reverse=True)

# Convert the sorted Excel file list to an HTML table
table_html = '<table class="table" id="new_linesheet_list">'
table_html += '''<thead><tr>
<th>Excel File</th>
<th class="text-center">Create Date</th>
<th class="text-center">Update Date</th>
<th class="text-center">Action</th>
</tr></thead>'''
table_html += '<tbody>'
for excel_file, creation_time, update_time in excel_files:
    table_html += '<tr class="ps-3">'
    table_html += '<td class="col-6"><input class="border-0 w-100" type="text" value="' + excel_file + '"></td>'
    table_html += '<td class="text-center">' + datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S') + '</td>'
    table_html += '<td class="text-center">' + datetime.fromtimestamp(update_time).strftime('%Y-%m-%d %H:%M:%S') + '</td>'
    table_html += '''<td class="text-center">
    <button class="border-0 bg-white" onclick="open_xlsm(&#39;'''+excel_file+'''&#39;)"><ion-icon name="open-outline"></ion-icon></button>
    <button class="border-0 bg-white" onclick="read_json_xlsm(&#39;'''+folder_name+'''/'''+excel_file+'''&#39;)"><ion-icon name="create-outline"></ion-icon></button>
    '''
    #  table_html += '''<td class="text-center">
    # <button class="border-0 bg-white" onclick="open_xlsm(&#39;'''+excel_file+'''&#39;)"><ion-icon name="open-outline"></ion-icon></button>
    # <button class="border-0 bg-white" onclick="read_json_xlsm(&#39;'''+folder_name+'''/'''+excel_file+'''&#39;)"><ion-icon name="create-outline"></ion-icon></button>
    # <button class="border-0 bg-white" onclick="remove_file()"><ion-icon name="trash-outline"></ion-icon></button></td>'''
    table_html += '</tr>'
table_html += '</tbody>'
table_html += '</table>'

# Return the HTML table
print(table_html)
