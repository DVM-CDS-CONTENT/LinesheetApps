import os

folder_path = "./"
folder_list = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

for asset in folder_list:
  print('<div onclick="get_linesheetlist(&#39;'+asset+'&#39;)"><ion-icon name="folder-outline" class="me-2"></ion-icon>'+asset+'</div>')