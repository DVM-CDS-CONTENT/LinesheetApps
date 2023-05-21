module.exports = {
  packagerConfig: {
   icon: 'my-app/src/image/icon/app/icon.png' // no file extension required
  },
  rebuildConfig: {},
  makers: [
    {
      name: '@electron-forge/maker-squirrel',
      config: {
        // An URL to an ICO file to use as the application icon (displayed in Control Panel > Programs and Features).
        // iconUrl: 'my-app/src/image/icon/app/icon.ico',
        // The ICO file to use as the icon for the generated Setup.exe
        // setupIcon: 'my-app/src/image/icon/app/icon.ico',
      },
    },
    {
      name: '@electron-forge/maker-zip',
      platforms: ['darwin'],
    },
    {
      // Path to a single image that will act as icon for the application
      name: '@electron-forge/maker-deb',
      config: {
      options: {
       icon: 'my-app/src/image/icon/app/icon.png',
      },},
    },
    {
      name: '@electron-forge/maker-rpm',
      config: {},
    },
  ],
  publishers: [
    {
      "name": "@electron-forge/publisher-github",
      "config": {
        "repository": {
          "owner": "24ep",
          "name": "spear"
        }
      }
    }
  ],
};

