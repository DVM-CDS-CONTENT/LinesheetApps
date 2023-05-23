const { contextBridge } = require('electron')



// var fs = require('fs');
// var { execSync } = require('child_process');
// var { execInstall } = require('child_process');

// var { exec } = require('child_process');
// var { promisify } = require('util');
// var { appendFile } = require('fs');
// var which = require('which');
// var https = require('https');


// exec('py -3.11 --version', (error, stdout, stderr) => {
//     if (error) {
//         // Notiflix.Loading.standard('install module path...');
//         console.log('Python is not installed.');

//         // Function to execute shell commands
//         const executeCommand = (command) => {
//             return new Promise((resolve, reject) => {
//                 exec(command, (error, stdout, stderr) => {
//                     if (error) {
//                         console.error(`Command execution failed: ${error}`);
//                         reject(error);
//                     } else {
//                         console.log(stdout);
//                         resolve();
//                     }
//                 });
//             });
//         };
//         const installPackage = async (packageName) => {
//             try {
//                 console.log(`Installing ${packageName}...`);
//                 await executeCommand(`py -3.11 -m pip install ${packageName}`);
//                 console.log(`${packageName} installation complete.`);
//             } catch (error) {
//                 console.error('An error occurred during installation:', error);
//             }
//         };

//         // Function to install Python and add it to environment variables
//         const installPython = async () => {
//             try {

//                 console.log('Installing Python...');
//                 await executeCommand('curl https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe -o python-3.11.2-amd64.exe');
//                 await executeCommand('python-3.11.2-amd64.exe /quiet InstallAllUsers=1 PrependPath=1');
//                 console.log('Python installation complete.');


//                 installPackage('mysql-connector-python');
//                 installPackage('numpy');
//                 installPackage('pandas');
//                 installPackage('sqlalchemy');
//                 installPackage('openpyxl==3.1.0');
//                 installPackage('pywin32');

//                 console.log('library installation complete.');
//                 // Notiflix.Loading.remove();
//                 // load_page(path.join(__dirname, 'page/linesheet/new_liensheet.html'));


//             } catch (error) {
//                 console.error('An error occurred during installation:', error);
//                 // Notiflix.Loading.remove();
//             }
//         };

//         // Call the installPython function
//         installPython();



//     } else {
//         console.log('Python version:', stdout);
//         // Notiflix.Loading.remove();

//     }
// });
