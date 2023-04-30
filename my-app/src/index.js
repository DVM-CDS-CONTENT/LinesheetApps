const { app, BrowserWindow, ipcMain, contextBridge  } = require('electron');
const path = require('path');
const fs = require('fs');
const { autoUpdater, AppUpdater } = require("electron-updater");

//Basic flags
autoUpdater.autoDownload = false;
autoUpdater.autoInstallOnAppQuit = true;

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
    icon :'/my-app/src/icon/app/app_window_bra.png',
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
  // Open the DevTools.
  mainWindow.webContents.openDevTools();
};
app.on('ready', () => {
  //update apps
  updateApp = require('update-electron-app');
  updateApp({
      updateInterval: '1 hour',
      notifyUser: true
  });


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
      if(filePath=='page/prompt_role.html'){
        event.sender.send('page-loaded', data);
      }
      if(filePath=='page/footers.html'){
        event.sender.send('footers-loaded', data);
      }
    });
  });
});

app.on('ready',createWindow);
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
