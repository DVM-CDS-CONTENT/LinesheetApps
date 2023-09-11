const { app, BrowserWindow, ipcMain, contextBridge , dialog , globalShortcut ,shell } = require('electron');
// Electron Builder
const { autoUpdater } =  require('electron-updater');

const path = require('path');
const fs = require('fs');

const { spawn ,spawnSync,execSync ,child_process } = require('child_process');

// Set the PYTHONHOME and PATH environment variables

  // process.env.PYTHONHOME = path.join(__dirname, '../../src/pythons');
  // process.env.PATH = `${process.env.PYTHONHOME};${process.env.PATH}`;

  // process.env.PYTHONHOME = path.join(__dirname, 'pythons');
  // process.env.PATH = `${process.env.PYTHONHOME};${process.env.PATH}`;

// const { autoUpdater, AppUpdater } = require("electron-updater");
process.env.GITHUB_TOKEN = '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';

// Handle creating/removing shortcuts on Windows when installing/uninstalling.
if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {

  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 600,
    minWidth:960,
    minHeight:600,
    frame:false,
    icon : path.join(__dirname, 'src/image/icon/app/icon.png') ,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
      contextIsolation:false
    },
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#262626',
      symbolColor: '#FFFFFF',
      height:28
    }
  });



  mainWindow.loadFile(path.join(__dirname, 'index.html'));

   // Register a global shortcut to toggle DevTools
   globalShortcut.register('CommandOrControl+Shift+I', () => {
    const webContents = mainWindow.webContents;
    if (webContents.isDevToolsOpened()) {
      webContents.closeDevTools();
    } else {
      webContents.openDevTools();
    }
  });

  // Open the DevTools.
  // mainWindow.webContents.openDevTools();

// Get the current window's webContents
  // const mainWindow = BrowserWindow.getFocusedWindow();
  const webContents = mainWindow.webContents;


  // const pythonScriptCode = "print('Hello, World!')";
  // runPythonScript(pythonScriptCode, webContents);

  // Set up auto-updater
  const server = 'https://dist.anystack.sh/v1/electron';
  const productId = '993ae19d-a245-4821-8574-2919694c3537';
  const url = `${server}/${productId}/releases`;


  // autoUpdater.setFeedURL({
  //   url: url,
  //   serverType: 'json',
  //   provider: 'generic',
  //   useMultipleRangeRequest: false
  // });

  // autoUpdater.checkForUpdatesAndNotify();


  // //  autoUpdater.checkForUpdates();

  // setInterval(() => {
  //   autoUpdater.checkForUpdatesAndNotify();
  //   // autoUpdater.checkForUpdates()

  //   webContents.executeJavaScript("console.log('checking');");
  // }, 100000)


  // // Event listeners for auto-updater
  // autoUpdater.on('checking-for-update', function() {
  //   webContents.executeJavaScript("console.log('Checking for updates...');");
  // });

  // autoUpdater.on('update-available', function(info) {
  //   webContents.executeJavaScript("console.log('Update available:', '"+info.version+"');");
  // });


  // autoUpdater.on('update-not-available', function() {
  //   webContents.executeJavaScript("console.log('No updates available.');");
  // });

  // autoUpdater.on('error', function(err) {
  //   webContents.executeJavaScript("console.error('Error in auto-updater:, "+err+"');");
  // });

  // autoUpdater.on('download-progress', function(progress) {

  //   webContents.executeJavaScript("console.log('Download progress :',"+Math.floor(progress.percent)+",'% downloaded');");
  // });

  // autoUpdater.on('update-downloaded', function(info) {
  //   webContents.executeJavaScript("console.log('Update downloaded:', '"+info.version+"');");
  //   // Optionally, you can trigger the installation of the update here.
  // });

  // autoUpdater.on('update-downloaded', (event, releaseNotes, releaseName) => {
  //   const dialogOpts = {
  //     type: 'info',
  //     buttons: ['Restart', 'Later'],
  //     title: 'Application Update',
  //     message: process.platform === 'win32' ? releaseNotes : releaseName,
  //     detail:
  //     'A new version has been downloaded. Restart the application to apply the updates.',
  //   }

  //   dialog.showMessageBox(dialogOpts).then((returnValue) => {
  //     if (returnValue.response === 0) autoUpdater.quitAndInstall()
  //   })
  // });


}





app.on('ready', async  () => {

  // Run a "Hello, World!" Python script when the Electron application is ready
  createWindow();

  const appUpdateYaml = `
  {
    url: 'https://dist.anystack.sh/v1/electron',
    serverType: 'json',
    provider: 'generic',
    useMultipleRangeRequest: false
  }
  `;



  try{
    fs.writeFileSync('resources/app-update.yml', appUpdateYaml);
  }catch (error) {
    // Code to handle the exception
  }


  //load div element
  ipcMain.on('load-file', (event, filePath) => {
    const fileFullPath = path.join(__dirname, filePath);
    fs.readFile(fileFullPath, 'utf8', (err, data) => {
      if (err) {
        console.error(`Error reading file ${fileFullPath}`, err);
        return;
      }
      if(filePath=='page/nav/welcome_nav.html'){
        event.sender.send('nav-loaded', data);
      }
      if(filePath=='page/installer_py.html'){
        event.sender.send('page-loaded', data);
      }
      if(filePath=='page/prompt_role.html'){
        event.sender.send('page-loaded', data);
      }
      if(filePath=='page/footers.html'){
        event.sender.send('footers-loaded', data);
      }
    });
  });



    // // Listen for the restart event
    // ipcMain.on('restart-app', () => {
    //   // app.relaunch();
    //   // app.quit();
    //   // app.relaunch({ args: process.argv.slice(1).concat(['--relaunch']) })

    //     // Relaunch the app after a short delay
    //   setTimeout(() => {
    //     // Spawn a new process to run the Electron app again
    //     spawn(process.execPath, [app.getPath('exe')], {
    //       detached: true,
    //       stdio: 'ignore',
    //     }).unref();
    //   }, 3000);
    //   app.quit();
    // });

    // shell.openExternal('https://docs.cdse-commercecontent.com/spear');

//  const guide = new BrowserWindow({
//   });

//   // Load a website URL
//   guide.loadURL('https://docs.cdse-commercecontent.com/spear');


});

// app.on('ready',createWindow);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {

  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
    const menu = Menu.buildFromTemplate(template)
    Menu.setApplicationMenu(menu)
    mainWindow.webContents.insertCSS(menuStyle)
  }
});

