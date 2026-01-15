# Manage the Lite Sync kDrive option (Windows)

Source: https://www.infomaniak.com/en/support/faq/2562/manage-the-lite-sync-kdrive-option-windows

---

This guide details the Lite Sync option of the kDrive desktop app (desktop application on Windows).

### Preamble

- The Lite Sync feature saves space by virtually storing your kDrive files on your computer, only downloading them when necessary.
- The files are always accessible from the kDrive web app (online service [kdrive.infomaniak.com](https://kdrive.infomaniak.com)) but locally they are present in a "dehydrated" way, requiring a loading time to be fully accessible.
- This allows you to view, complete, and synchronize the content of kDrive without saturating the hard drive.
- The Lite Sync option always acts:on a specific kDrive (in the case where you synchronize several on the application).and on the entirety of the kDrive (or the entirety of an advanced synchronization).and via a specific kDrive app (another user of the same kDrive can make a different Lite Sync choice than yours).

## Enable the Lite Sync option

### Prerequisites & scope of use of Lite Sync

- OS Windows version ≥ 10 (21h2)
- not available with Linux
- 64-bit processor (ARM64 compatible)
- File storage system under NTFS / APFS

The Lite Sync option can be enabled during the installation of the application (this is offered to you) or subsequently:

1. Left-click the app icon in the notification area of your computer (bottom right on Windows).
2. Click the action menu ⋮ to the right of the kDrive window.
3. Select kDrive Settings.
4. Click the button in the *Synchronization* section to enable Lite Sync.

The cloud icon
 will appear to the far right of a sync name on the application, indicating that Lite Sync is enabled. If the crossed-out cloud icon
 is displayed, this means that Lite Sync is not enabled:

#### Keep on this device

Once Lite Sync is enabled, you can still make a folder and its subfolders or only one or more subfolders available locally:

1. From the Windows Explorer, navigate to a folder synchronized with kDrive and right-click.
2. Select the Keep on this device option under kDrive:

#### Free up space

Conversely, once Lite Sync is enabled, you can free up space in a folder and its subfolders or only in one or more subfolders.

> **Note:** Warning: "free up space" is not applied by default to new files or folders added locally.

1. From the Windows Explorer, navigate to a folder synchronized with kDrive and right-click
2. Select the Free up space option under kDrive:

> **Note:**  The action Free up space will free up storage space on your computer. Files will remain visible but will no longer be accessible without an internet connection.

## Usage example #1 (required storage space)

If you enable Lite Sync, the space occupied (e.g. 900 GB) on the Infomaniak server will be freed up on your hard drive, but the reverse is also true (e.g. 900 GB of free space required on your hard drive if the Lite Sync option is activated along the way).

> **Note:** Therefore, it is recommended to keep the initial choice of activating or not activating Lite Sync, and not to change it along the way.

### File "dehydration"

As explained in the preamble, a dehydrated file is a kDrive file whose complete version is not present on the hard drive and instead a 1 KB "shortcut" is displayed, which is normal behavior when Lite Sync is activated.

In some cases (e.g. if you copy the files from your hard drive while Lite Sync is activated, and then start a new synchronization to a new kDrive) the application will block the import of this type of file. To resolve these errors, you can download the complete file from the kDrive web app (online service [kdrive.infomaniak.com](https://kdrive.infomaniak.com/)).

## Usage example #2 (icon summary)

Files on the hard drive synchronized with the Lite Sync option, everything is in the cloud (on your remote online kDrive):

Deactivation of the LiteSync option, the "physical" synchronization starts:

Synchronization complete, the files have been downloaded to your computer and then have the appropriate icon:

To summarize, here are the status icons used in your Windows Explorer:

## Disable the Lite Sync option

To do this:

1. Left-click on the app icon in the notification area of your computer (bottom right on Windows).
2. Click on the action menu ⋮ to the right of the kDrive window.
3. Select kDrive Settings.
4. Click on the button in the *Synchronization* section to disable Lite Sync.
5. Two scenarios may occur:If there is enough space on your computer, a message confirming the deactivation is displayed; simply click on Continue. If there is not enough space on your computer, a message will indicate the missing space to allow the deactivation of Lite Sync; the synchronization of your kDrive will be paused until you select the files to synchronize on your computer.
