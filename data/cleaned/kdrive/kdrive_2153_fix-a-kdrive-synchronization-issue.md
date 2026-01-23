# Fix a k Drive synchronization issue

Source: https://www.infomaniak.com/en/support/faq/2153/fix-a-kdrive-synchronization-issue

---

This guide helps resolve certain cases where you notice that [k Drive](https://infomaniak.com/gtl/kdrive) data is not synchronized between your devices.

## Running k Drive in the background

For k Drive synchronization to work when there is an update to your k Drive data (new file, edited document, etc.), it is obviously necessary for the **k Drive** app to be open (and for you to be logged in with the correct user account, etc.).

### On Windows: Access the k Drive icon for verification

To check if the k Drive app is running on a Windows computer, you need to locate the folder icon
![image](https://faq.storage5.infomaniak.com/4d6627a80753537ac120fe2da401467c40a122de.png)
 in the notification area.

1. If necessary, open the k Drive software installed on your computer: Click on the Start menu to open it. Search for kdrive. The search result should display the k Drive app (otherwise reinstall the application). Open the k Drive app by clicking on Open or Run as administrator:
2. **The app icon should be visible**in the notification area of your computer at the bottom right on Windows.
3. If it is not there: Locate the small arrow (or chevron) that indicates hidden icons: Click on this arrow to expand the notification area. The hidden icons will then appear, allowing you to view the desired application: You can also check the notification area customization settings in Windows system settings.
4. Click on the icon to access your k Drive synchronization settings and information:

![image](https://faq.storage5.infomaniak.com/d9f056983ae3483439d66210b55a9aa6bdc356ce.png)

### On Android: k Drive and background operation

When you import large files or multiple files into k Drive, this can take several minutes. To ensure data import, the mobile **k Drive** app needs to be able to continue this task when you close the application or open another one. The **automatic photo backup** function in k Drive may also be disrupted if the app cannot run in the background.

Due to the power management policy on some devices of certain manufacturers (especially Chinese ones), applications not on their whitelist may be automatically stopped, preventing certain tasks from functioning properly.

You can work around this issue by following the instructions available in English on the site *don't kill my app* at the address [dontkillmyapp.com](https://dontkillmyapp.com/):

- [Asus](https://dontkillmyapp.com/asus)
- [Huawei](https://dontkillmyapp.com/huawei)
- [Lenovo](https://dontkillmyapp.com/lenovo)
- [Meizu](https://dontkillmyapp.com/meizu)
- [Oneplus](https://dontkillmyapp.com/oneplus)
- [Oppo](https://dontkillmyapp.com/oppo)
- [Samsung](https://dontkillmyapp.com/samsung)
- [Vivo](https://dontkillmyapp.com/vivo)
- [Xiaomi](https://dontkillmyapp.com/xiaomi)

Don't see your phone's brand? Then your phone is probably not causing any issues.

## Missing folders on the computer

If everything seems fine…

- … no synchronization interrupted
- … no error messages
- … you have the necessary access rights when you view them in their online version ([ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive))

but you notice that…

- … folders like the *Organization folders* (shared folders) or other directories are not visible on your computer…

then check on the desktop app **k Drive** installed on your computer the setting that allows you to limit the synchronization of large folders (`500 Mo` by default):

1. Left-click on the desktop app icon in the notification area of your computer (top right on **macOS**, bottom right on **Windows** and a double left-click in the taskbar on **Linux**).
2. Click on the action menu **⋮** on the right of the window that appears.
3. Click on **App preferences**.
4. Disable the toggle switch to have no limits on the size of synchronized folders:

![sign](https://faq.storage.infomaniak.com/661540cfddfb60.95169324gif)

Then check on the desktop app **k Drive** installed on your computer [which folders you want to synchronize](https://www.infomaniak.com/en/support/faq/2454):

1. Left-click on the desktop app icon in the notification area of your computer (top right on **macOS**, bottom right on **Windows** and a double left-click in the taskbar on **Linux**).
2. Click on the action menu **⋮** on the right of the window that appears.
3. Click on **k Drive settings**.
4. Click to the left of the name of your synchronization to expand the folder tree of the folders contained.
5. Activate the boxes corresponding to the folders that are not yet synchronized as you wish.
6. Validate with the blue button:

![sign](https://faq.storage.infomaniak.com/661541b09953e6.29170974gif)

The result will be that your local folder representing k Drive (named *k Drive*, or *k Drive2*, or other) on the computer, will finally display all the desired folders (after the necessary time for synchronization).

## Synchronization in progress (0/10) then on pause

Check that the **Windows Search** service is not stopped. Proceed through the **Run** window (Win + R):

1. Enter `services.msc`.
2. Click OK:

![image](https://faq.storage5.infomaniak.com/82927361b8d231b12253fe4823a41ab920fab432.png)

3. Locate **Windows Search** in the list of the **Services** window and activate it if it is not already:

![image](https://faq.storage5.infomaniak.com/2517f7a8ca6d144d3df4278c517ca63d5094d697.png)

## Continuous synchronization (files .eml)

A problem [related to Windows indexing](https://www.sevenforums.com/browsers-mail/35334-eml-files-timestamps-updated-constantly.html) may occur during the synchronization of **k Drive** files with the `.eml` extension (a file type corresponding to [email export/save](https://www.infomaniak.com/en/support/faq/973)). It is therefore necessary to remove the `eml` type from the indexing options to resolve this issue:

1. Open the **Start** menu and search for indexing options.
2. Click on **Indexing Options** (Control Panel):

![image](https://faq.storage5.infomaniak.com/b6af908d40e7489151cde8beccc686def51355fa.png)

3. Click on the **Advanced** button.
4. Uncheck the box for the `eml` type:

![image](https://faq.storage5.infomaniak.com/c82edc983e68d1ab34027ca4628908b4810c06f7.png)

5. Validate and close the windows.

## Adobe file synchronization

Adobe applications such as **Illustrator**, **Photoshop**, **Lightroom**, etc. encounter issues when saving files (Adobe software error messages, file duplication, etc.) on k Drive. Therefore, it is best to avoid including Adobe files in a synchronization.

Adobe [explicitly states](https://helpx.adobe.com/illustrator/kb/illustrator-support-networks-removable-media.html) that it does not support cloud synchronizations, external drives, and network drives.