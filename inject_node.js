// This file is for JS injected into node runtime

// Hide the debugger (in case they find out about this)
process.argv = [process.argv[0]]

// Disable highly advanced locking system
main_window = require("electron").BrowserWindow.getAllWindows()[0]
main_window.fullScreenable = false

// Open devtools on launch
main_window.webContents.toggleDevTools()