# Move kDrive local location

Source: https://www.infomaniak.com/en/support/faq/2856/move-kdrive-local-location

---

This guide explains how to change the local location used by the desktop app [kDrive](https://infomaniak.com/gtl/kdrive) (desktop application on macOS / Windows / Linux) to, for example, store synchronized data **on another hard drive** when the initially chosen one no longer has enough space.

### Preamble

- Indeed, if the *Lite Sync* option is not enabled, all existing data on the Web app **kDrive** (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) are also present locally on the synchronized device and **take up storage space**.As the volume of data can be very large, you may need to store the data on a different hard drive than the one initially chosen.
- **Never move a folder used for kDrive synchronization**‍ (`/kdrive`, `/kdrive2`, etc.) whether the kDrive application is open or closed or uninstalled for the purpose of being reinstalled.If everything is synchronized, then you need to delete the folder and recreate it as explained below.If you proceed differently by using a folder that already contains your data, you expose yourself to file conflicts.

## Modify the local directory used by kDrive

To set a new folder for kDrive synchronization when the initially chosen first folder is no longer to be used, follow this procedure:

1. Make sure all your data is synchronized and actually exists by being visible on the Web app **kDrive** (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. If necessary, locate the folder currently used by the desktop app **kDrive** (click on **Drive Settings** from the application, then click on the blue URL displayed under **Folders** to open the local folder and thus locate its location):

![image](https://faq.storage5.infomaniak.com/af2a336812f38ced18dbceec346ebfb7069f85f0.png)

3. **Quit** the desktop app kDrive on the device where you want to change the folder used:

![image](https://faq.storage5.infomaniak.com/ed40d46d127a075a40f2963c1de5681d843598d1.png)

4. Completely uninstall the desktop app kDrive by **deleting all configuration/settings data**, etc. — on macOS, use **kDrive Uninstaller** present in the Applications/kDrive folder):

![image](https://faq.storage5.infomaniak.com/2f655f27de66be2a2b472ce3dd99789636819d30.png)

5. Delete the folder `kDrive` (or `kDrive2`, etc. located in step 2).
6. [Reinstall](http://infomaniak.com/gtl/ksuite.kdrive.apps) the desktop app **kDrive** and when the user account connection is made, click on the **pencil** icon ✎ at the folder selection step:

![image](https://faq.storage5.infomaniak.com/9c2a9aabec2cfb688dbf1e3f3b6040429a5fb550.png)

7. Choose the new hard drive as the location of the new folder (name it as you wish):

![image](https://faq.storage5.infomaniak.com/0e3a5dc0d7983b2b86854cf6a3bd45fb95ed9fd8.png)

8. Complete the configuration:

![image](https://faq.storage5.infomaniak.com/a696b29935bab3d68a2f85d438eea406fb54925f.png)

9. The download of the kDrive data present on the Infomaniak servers will begin and continue entirely in the background.Refer to this other guide to download only certain specific folders.