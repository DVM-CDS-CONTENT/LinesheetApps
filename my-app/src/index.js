const { app, BrowserWindow } = require('electron');
const path = require('path');

// const electron = require('electron');
// const remote = electron.remote;

const { PythonShell } = require('python-shell');





// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true // Required to use Node.js modules in the renderer process
    },
  });


  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Open the DevTools.
  mainWindow.webContents.openDevTools();
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  // On OS X it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and import them here.

app.on('session-created',()=> {
    const page_loaded = sessionStorage.getItem('page_loaded');
        if(page_loaded=='page/linesheet_page.html'){

// Run the Python script with the function and arguments
PythonShell.run('python.py', {args: ['get_family']}, (err, [data]) => {
    if (err) throw err;
    document.getElementById("template_options").innerHTML = data;
});

PythonShell.run('python.py', {args: ['get_xlsx']}, (err, [data]) => {
    if (err) throw err;
    document.getElementById("exist_linesheet").innerHTML = data;
});

PythonShell.run('python.py', {args: ['get_input',JSON.stringify('sale_channel','multiple')]}, (err, [data]) => {
    if (err) throw err;
    document.getElementById("sale_channel_options").innerHTML = data;
});

PythonShell.run('python.py', {args: ['get_input',JSON.stringify('production_type','single')]}, (err, [data]) => {
    if (err) throw err;
    document.getElementById("production_type_options").innerHTML = data;
});



PythonShell.run('python.py', {args: ['get_input',JSON.stringify('stock_source','multiple')]}, (err, [data]) => {
    if (err) throw err;
    document.getElementById("stock_source_options").innerHTML = data;
    new SlimSelect({
        select: '#stock_source_show',
        settings: {
            closeOnSelect: false,
            allowDeselectOption: true,
        },
        events: {
            afterChange: (newVal) => {
                var input_update ="";
                for (let i = 0; i < newVal.length; i++) {
                    if(input_update==""){
                        input_update = newVal[i].value;
                    }else{
                        input_update = input_update +','+newVal[i].value;
                    }
                }
                document.getElementById("stock_source").value = input_update;
            }
        }
    })
    new SlimSelect({
        select: '#template_show',
        settings: {
            closeOnSelect: false,
            allowDeselectOption: true,
        },
        events: {
            afterChange: (newVal) => {
                var input_update ="";
                for (let i = 0; i < newVal.length; i++) {
                    if(input_update==""){
                        input_update = newVal[i].value;
                    }else{
                        input_update = input_update +','+newVal[i].value;
                    }
                }
                document.getElementById("template").value = input_update;
            }
        }
    })
    new SlimSelect({
        select: '#sale_channel_show',
        settings: {
            closeOnSelect: false,
            allowDeselectOption: true,
        },
        events: {
            afterChange: (newVal) => {
                var input_update ="";
                for (let i = 0; i < newVal.length; i++) {
                    if(input_update==""){
                        input_update = newVal[i].value;
                    }else{
                        input_update = input_update +','+newVal[i].value;
                    }
                }
                document.getElementById("sale_channel").value = input_update;
            }
        }
    })
    new SlimSelect({
        select: '#production_type_show',
        settings: {
            closeOnSelect: false,
            allowDeselectOption: true,
        },
        events: {
            afterChange: (newVal) => {
                var input_update ="";
                for (let i = 0; i < newVal.length; i++) {
                    if(input_update==""){
                        input_update = newVal[i].value;
                    }else{
                        input_update = input_update +','+newVal[i].value;
                    }
                }
                document.getElementById("production_type").value = input_update;
            }
        }
    })

});


        }
})


