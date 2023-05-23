
// URL to the Python installer
const pythonInstallerURL = 'https://example.com/python-installer.exe';

// Path to the downloaded Python installer
const pythonInstallerPath = path.join(__dirname, 'python-installer.exe');

// Function to check if Python is installed
function isPythonInstalled() {
  try {
    // Attempt to execute the `python` command
    execSync('python --version');
    return true;
  } catch (error) {
    return false;
  }
}

// Function to add Python to user environment path
function addPythonToPath() {
  try {
    const pythonPath = path.dirname(pythonInstallerPath); // Assuming pythonInstallerPath is defined correctly
    execSync(`setx /m PATH "%PATH%;${pythonPath}"`);
    console.log('Python added to user environment path successfully.');
  } catch (error) {
    console.error('Error adding Python to user environment path:', error);
  }
}

// Function to download the Python installer
function downloadPythonInstaller() {
  console.log('Downloading Python installer...');
  const file = fs.createWriteStream(pythonInstallerPath);
  https.get(pythonInstallerURL, (response) => {
    response.pipe(file);
    file.on('finish', () => {
      file.close();
      console.log('Python installer downloaded successfully.');
      installPython();
    });
  }).on('error', (error) => {
    fs.unlinkSync(pythonInstallerPath);
    console.error('Error downloading Python installer:', error);
  });
}

// Function to install Python
function installPython() {
  try {
    console.log('Installing Python...');
    execSync(`"${pythonInstallerPath}" /silent`);
    console.log('Python installation completed successfully.');
  } catch (error) {
    console.error('Error installing Python:', error);
  }
}

// Check if Python is already installed
if (isPythonInstalled()) {
  console.log('Python is already installed.');
} else {
  // Python is not installed, so we proceed with installation
    downloadPythonInstaller();
    addPythonToPath();
}
