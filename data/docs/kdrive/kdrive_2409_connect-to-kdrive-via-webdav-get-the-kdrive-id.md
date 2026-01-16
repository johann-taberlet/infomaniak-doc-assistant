# Connect to kDrive via WebDAV (get the kDrive ID)

Source: https://www.infomaniak.com/en/support/faq/2409/connect-to-kdrive-via-webdav-get-the-kdrive-id

---

This guide provides instructions to connect to [kDrive](https://infomaniak.com/gtl/kdrive) using the WebDAV connection protocol.

**⚠ Available with:**

### Preamble

- Connecting via WebDAV allows you to:use the WebDAV application of your choice instead of the official kDrive application (only solution if this one is unavailable on your OS, for example macOS 10.14.6),use kDrive as a synchronization base for a tool that would allow this via WebDAV (Joplin for example),access kDrive from your operating system's file manager.

## Obtain the identifier (kDrive ID)

To find out your kDriveID, kDrive client ID:

1. [Click here](https://ksuite.infomaniak.com/kdrive) to access the Infomaniak kDrive web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. The kDrive directory structure is displayed in the left sidebar menu.
3. The URL `https://ksuite.infomaniak.com/kdrive/app/drive/123456/` displayed at the top of your browser contains a number:

![image](https://faq.storage5.infomaniak.com/c0d1f008cc4d19c9630f43a59bdfd81905998d32.png)

4. In some cases, especially when the Organization ID is mentioned in the URL, there may be several series of numbers, but the principle remains the same, you need to take the number displayed after the term “`/drive/`”:

![image](https://faq.storage5.infomaniak.com/a1e2af5e6b6dfb9bfe34fe55882e705a7465fcd3.png)

This number (in the example `123456`) is your kDrive identifier (*IDkDrive*).

You will therefore need to write https://*IDkDrive*.connect.kdrive.infomaniak.com each time it is necessary (`https://123456.connect.kdrive.infomaniak.com` for example as a WebDAV web address).

## Connect to kDrive via WebDAV…

> **Note:** **Not all offers are WebDAV compatible. Please refer to the box at the top of the page.**

### … on Windows

To do this:

1. Open the **File Explorer** from the taskbar or the Start menu.
2. Select **This PC** in the left pane.
3. In the **Computer** tab, select **Add a network location**:

![image](https://faq.storage5.infomaniak.com/f1b6551ff42be8d98eaf929e0540d4ea60f6274e.png)

4. Click on **Next**.
5. Click on **Choose a custom network location**:
 
![image](https://faq.storage5.infomaniak.com/deff5dad94635d59f541e142b3bcbdd1c5a6f4db.png)

6. Click on **Next**.
7. Enter the **server address**: `https://IDkDrive.connect.kdrive.infomaniak.com` (see the ID kDrive chapter above).
8. Click on **Next**.
9. For the account settings, use the following information:Server address: https://IDkDrive.connect.kdrive.infomaniak.com (see the ID kDrive chapter above).Username: email address to log in to your Infomaniak accountPassword: create an application password for this specific use.
10. If desired, click the box to save the login information.
11. Enter a name for this connection or leave the default indication.
12. Click on **Finish**.
13. Two folders will appear, one containing deleted files & folders, the other with the name of your kDrive and containing your data.

### … on macOS

For a computer on macOS, follow the [Apple instructions](https://support.apple.com/fr-ch/guide/mac-help/mchlp1546/mac), which can result in this:

1. Click on the **Go** menu from the Finder.
2. Click on **Connect to server**:

![image](https://faq.storage5.infomaniak.com/716ba50f12e7b2d439bc9d3878d4ed0fdac65384.png)

3. Enter the **server address**: `https://IDkDrive.connect.kdrive.infomaniak.com` (see the ID kDrive chapter above).
4. Click on **Connect**:

![image](https://faq.storage5.infomaniak.com/fde2cccf409a13541818f57ac19b61d3040fb30d.png)

5. Confirm the connection by clicking on the blue button.
6. Enter the following information:Username: email address to log in to your Infomaniak accountPassword: create an application password for this specific use.
7. If desired, click the box to save the login information.
8. Click on the blue button to connect:

![image](https://faq.storage5.infomaniak.com/65cf36bf3b5f8f75e95c73c1831057f906632e6c.png)

9. There you go, the kDrive content is displayed on the Finder:

![image](https://faq.storage5.infomaniak.com/d31c4d7f658c596f5f3f6889f2fbaa7574325e49.png)

### ... on Linux (Gnome)

To do this:

1. Open **Files.**
2. In the sidebar, click on **Network**:

![image](https://faq.storage5.infomaniak.com/c8a6be58f9ca0550f03cb93fd71fc7450db2e496.png)

3. Enter the **server address**: `davs://IDkDrive.connect.kdrive.infomaniak.com` (read the kDrive ID chapter above).
4. Click on **Connect**.
5. For the account settings, use the following information:Username: email address to log in to your Infomaniak accountPassword: create an application password for this specific use.
6. Click on **Login**.

### ... with a Windows software

Use the [RaiDrive](https://www.raidrive.com/) software for quick access to your hosted data. Complete the fields as in the image below:

![image](https://faq.storage5.infomaniak.com/8c888e032f44ff022c32abce9c142c030aceefaf.png)

### ... with a Windows / macOS software

Use the [Cyberduck](https://cyberduck.io/) software for quick access to your hosted data:

1. Open **Cyberduck**.
2. In the software menu, go to **Bookmark** then to **New bookmark**.
3. Select the **WebDAV (https)** protocol.
4. Provide the following information:Server address: https://IDkDrive.connect.kdrive.infomaniak.com (see the ID kDrive chapter above)Username: email address to log in to your Infomaniak accountPassword: create an application password for this specific use.Download folder: the folder where downloaded files will be stored

> **Note:** Most recent software supporting the WebDAV protocol is compatible with kDrive offers among those also supporting WebDAV. Infomaniak cannot guarantee the compatibility of the service with external applications and **does not provide support for this protocol**. It is recommended to [install the kDrive application](https://www.infomaniak.com/en/support/faq/2374) to avoid any file loss.

## Direct WebDAV connection URL to a specific folder

To facilitate a direct connection via WebDAV to a specific folder, you can use the following URL:

`https://IDkDrive.connect.kdrive.infomaniak.com/Common documents/Nom du dossier`

This simple method allows you to quickly access the desired folder without manually navigating the directory structure. Simply replace "`Folder name`" with the exact name of the target folder to establish a direct and secure connection via WebDAV. Also, refer to the last part of [this other guide](https://www.infomaniak.com/en/support/faq/2557) for other examples.