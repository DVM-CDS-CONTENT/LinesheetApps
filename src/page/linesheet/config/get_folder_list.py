import os

folder_path = "./"
os_path=os.listdir(folder_path)
folder_list = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]

i = 0
for asset in folder_list :
    if asset!='out' and asset!='src' and asset!='node_modules':
        i = i + 1

        folder_path_os = os.path.abspath(asset)
        folder_path_os = folder_path_os.replace('\\', '\\\\')
        # print(folder_path_os)
        # folder_path_os = os.path.join(*folder_path_os.split('/'))

        print('''


                <div class="nav-item dropdown dropend">
                <a class="element w-100 p-3 pb-1 pt-1 fw-700 nav-link dropdown-toggle" style="font-size:13px" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <ion-icon name="folder-outline" class="me-2"></ion-icon>'''+asset+'''
                </a>
                    <ul class="dropdown-menu dropdown-menu rounded-0 shadow-sm" aria-labelledby="navbarDarkDropdownMenuLink">
                        <li><a class="dropdown-item" style="font-size:13px" onclick="get_linesheetlist(&#39;'''+asset+'''&#39;)">Open folder</a></li>
                        <li><a class="dropdown-item" style="font-size:13px" onclick="revealInFileExplorer(&#39;'''+folder_path_os+'''&#39;)">Reveal in File Explorer</a></li>
                        <li><a class="dropdown-item" style="font-size:13px" onclick="removeFolder(&#39;'''+asset+'''&#39;)" >Remove</a></li>
                    </ul>
                </div>



                ''')
print(''' <hr>
    <button type="button" class="border-0 w-100  ms-2 bg-white " style="font-size:13px;text-align: -webkit-left;" onclick="prompt_folder_name_create()">              <ion-icon name="add-outline" role="img" class="md hydrated"></ion-icon> Create new folder    </button>''')