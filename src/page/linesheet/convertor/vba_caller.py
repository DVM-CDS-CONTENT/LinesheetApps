import win32com.client
import sys
import os
import re


def run_vba_code(file_path, macro_name):
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False  # Set to True if you want to see Excel

        # Convert to an absolute path
        abs_file_path = os.path.abspath(file_path)

        workbook = excel.Workbooks.Open(abs_file_path)
        # Check if the macro exists in the workbook
        if not excel.Application.Run(f"{workbook.Name}!{macro_name}"):
            print("Macro '{macro_name}' not found in the workbook.")
        else:
        # Run VBA code
            excel.Application.Run(f"{workbook.Name}!{macro_name}")

            print(workbook.Sheets('IN_LINK_DATA').Cells(16, 2).Value)
            print(workbook.Sheets('IN_LINK_DATA').Cells(17, 2).Value)
            print("Passed : finnish validation linesheet")
            
    except Exception as e:

        print("Warning : Validation macro "+macro_name+" not available in the workbook.")

    finally:
        # Restore DisplayAlerts to its default value
        excel.DisplayAlerts = True
        workbook.Save()

        # Close the workbook without saving changes (optional)
        workbook.Close(False)

        # Quit Excel application
        excel.Quit()
        


file_path = sys.argv[1]
macro_name = 'Sheet1.RunValidation'



run_vba_code(file_path, macro_name)

