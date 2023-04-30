const { contextBridge } = require('electron')
let { PythonShell } = require('python-shell')
// contextBridge.exposeInMainWorld(PythonShell)

// Good code
contextBridge.exposeInMainWorld('preload', {
  PythonShell: () => run()
})