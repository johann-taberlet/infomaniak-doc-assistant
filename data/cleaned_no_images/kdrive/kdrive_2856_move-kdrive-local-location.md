# Move k Drive local location

Source: https://www.infomaniak.com/en/support/faq/2856/move-kdrive-local-location

---

This guide explains how to change the local location used by the desktop app [k Drive](https://infomaniak.com/gtl/kdrive) (desktop application on macOS / Windows / Linux) to, for example, store synchronized data **on another hard drive** when the initially chosen one no longer has enough space.

### Preamble

- Indeed, if the *Lite Sync* option is not enabled, all existing data on the Web app **k Drive** (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) are also present locally on the synchronized device and **take up storage space**. As the volume of data can be very large, you may need to store the data on a different hard drive than the one initially chosen.
- **Never move a folder used for k Drive synchronization** (`/kdrive`, `/kdrive2`, etc.) whether the k Drive application is open or closed or uninstalled for the purpose of being reinstalled. If everything is synchronized, then you need to delete the folder and recreate it as explained below. If you proceed differently by using a folder that already contains your data, you expose yourself to file conflicts.

## Modify the local directory used by k Drive

To set a new folder for k Drive synchronization when the initially chosen first folder is no longer to be used, follow this procedure:

1. Make sure all your data is synchronized and actually exists by being visible on the Web app **k Drive** (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. If necessary, locate the folder currently used by the desktop app **k Drive** (click on **Drive Settings** from the application, then click on the blue URL displayed under **Folders** to open the local folder and thus locate its location):

3. **Quit** the desktop app k Drive on the device where you want to change the folder used:

4. Completely uninstall the desktop app k Drive by **deleting all configuration/settings data**, etc. — on macOS, use **k Drive Uninstaller** present in the Applications/k Drive folder):

5. Delete the folder `k Drive` (or `k Drive2`, etc. located in step 2).
6. [Reinstall](http://infomaniak.com/gtl/ksuite.kdrive.apps) the desktop app **k Drive** and when the user account connection is made, click on the **pencil** icon ✎ at the folder selection step:

7. Choose the new hard drive as the location of the new folder (name it as you wish):

8. Complete the configuration:

9. The download of the k Drive data present on the Infomaniak servers will begin and continue entirely in the background. Refer to this other guide to download only certain specific folders.