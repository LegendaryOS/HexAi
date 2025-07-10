const { app, BrowserWindow, ipcMain } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let backendProcess;
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    icon: path.join(__dirname, 'frontend/assets/logo.png'),
  });

  mainWindow.loadFile('frontend/index.html');

  // Spawn backend process
  backendProcess = spawn('python3', ['backend/main.py'], { stdio: ['pipe', 'pipe', 'pipe'] });
  backendProcess.stdout.on('data', (data) => {
    console.log(`Backend: ${data}`);
  });
  backendProcess.stderr.on('data', (data) => {
    console.error(`Backend Error: ${data}`);
  });

  mainWindow.on('closed', () => {
    backendProcess.kill();
    mainWindow = null;
  });

  // Maximize window
  mainWindow.maximize();
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// Handle offline mode
ipcMain.handle('check-backend', async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/history');
    return response.ok;
  } catch {
    return false;
  }
});
