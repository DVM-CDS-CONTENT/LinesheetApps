const { app, BrowserWindow, ipcMain, contextBridge  ,autoUpdater} = require('electron');

const path = require('path');
const fs = require('fs');
const { autoUpdater, AppUpdater } = require("electron-updater");


process.env.GITHUB_TOKEN = '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';


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
    icon :'src/image/icon/app/icon.png',
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
  // mainWindow.webContents.openDevTools();
};

// const { app, autoUpdater } = require('electron')
autoUpdater.setFeedURL('https://dist.unlock.sh/v1/electron/9934de97-8f51-4518-8c9d-7fad7a0006c7')
autoUpdater.checkForUpdates()

setInterval(() => {
  autoUpdater.checkForUpdates()
}, 30000)

autoUpdater.on('update-downloaded', (event, releaseNotes, releaseName) => {
  // autoUpdater.quitAndInstall()
console.log('update installed')
})

app.on('ready', () => {


  // autoUpdater.checkForUpdates()
  autoUpdater.checkForUpdatesAndNotify()

  // if (process.env.WEBPACK_DEV_SERVER_URL) {
  //     // Load the url of the dev server if in development mode
  //     win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
  //     if (!process.env.IS_TEST) win.webContents.openDevTools()
  // } else {
  //   const server = 'https://dist.anystack.sh/v1/electron'
  //   const productId = '9934de97-8f51-4518-8c9d-7fad7a0006c7'
  //   const url = `${server}/${productId}/releases`

  //     autoUpdater.setFeedURL({
  //         url: url,
  //         serverType: 'json',
  //         provider: "generic",
  //         useMultipleRangeRequest: false
  //     })

  //     autoUpdater.checkForUpdatesAndNotify()
  // }

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
