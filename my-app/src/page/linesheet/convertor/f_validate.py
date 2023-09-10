# def check_function_existence(file_path, function_name):
#     with open(file_path, 'r') as file:
#         code = file.read()

#     function_lines = [line for line in code.split('\n') if 'def ' in line]
#     function_names = [line.split('def ')[1].split('(')[0].strip() for line in function_lines]

#     if function_name in function_names:
#         return 1
#     else:
#         return function_name + " does not exist"

# # Usage example:
# result = check_function_existence('src/page/linesheet/convertor/f_convert.py', 'description')
# print(result)
