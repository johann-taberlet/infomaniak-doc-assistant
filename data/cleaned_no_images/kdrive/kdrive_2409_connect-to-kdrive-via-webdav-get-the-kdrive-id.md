# Connect to k Drive via WebDAV (get the k Drive ID)

Source: https://www.infomaniak.com/en/support/faq/2409/connect-to-kdrive-via-webdav-get-the-kdrive-id

---

This guide provides instructions to connect to [k Drive](https://infomaniak.com/gtl/kdrive) using the WebDAV connection protocol.

**⚠ Available with:**

### Preamble

- Connecting via WebDAV allows you to:use the WebDAV application of your choice instead of the official k Drive application (only solution if this one is unavailable on your OS, for example macOS 10.14.6),use k Drive as a synchronization base for a tool that would allow this via WebDAV (Joplin for example),access k Drive from your operating system's file manager.

## Obtain the identifier (k Drive ID)

To find out your k DriveID, k Drive client ID:

1. [Click here](https://ksuite.infomaniak.com/kdrive) to access the Infomaniak k Drive web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. The k Drive directory structure is displayed in the left sidebar menu.
3. The URL `https://ksuite.infomaniak.com/kdrive/app/drive/123456/` displayed at the top of your browser contains a number:

4. In some cases, especially when the Organization ID is mentioned in the URL, there may be several series of numbers, but the principle remains the same, you need to take the number displayed after the term “`/drive/`”:

This number (in the example `123456`) is your k Drive identifier (*IDk Drive*).

You will therefore need to write https://*IDk Drive*.connect.kdrive.infomaniak.com each time it is necessary (`https://123456.connect.kdrive.infomaniak.com` for example as a WebDAV web address).

## Connect to k Drive via WebDAV…

> **Note:** **Not all offers are WebDAV compatible. Please refer to the box at the top of the page.**

### … on Windows

To do this:

1. Open the **File Explorer** from the taskbar or the Start menu.
2. Select **This PC** in the left pane.
3. In the **Computer** tab, select **Add a network location**:

4. Click on **Next**.
5. Click on **Choose a custom network location**:

6. Click on **Next**.
7. Enter the **server address**: `https://IDk Drive.connect.kdrive.infomaniak.com` (see the ID k Drive chapter above).
8. Click on **Next**.
9. For the account settings, use the following information: Server address: https://IDk Drive.connect.kdrive.infomaniak.com (see the ID k Drive chapter above). Username: email address to log in to your Infomaniak account Password: create an application password for this specific use.
10. If desired, click the box to save the login information.
11. Enter a name for this connection or leave the default indication.
12. Click on **Finish**.
13. Two folders will appear, one containing deleted files & folders, the other with the name of your k Drive and containing your data.

### … on macOS

For a computer on macOS, follow the [Apple instructions](https://support.apple.com/fr-ch/guide/mac-help/mchlp1546/mac), which can result in this:

1. Click on the **Go** menu from the Finder.
2. Click on **Connect to server**:

3. Enter the **server address**: `https://IDk Drive.connect.kdrive.infomaniak.com` (see the ID k Drive chapter above).
4. Click on **Connect**:

5. Confirm the connection by clicking on the blue button.
6. Enter the following information: Username: email address to log in to your Infomaniak account Password: create an application password for this specific use.
7. If desired, click the box to save the login information.
8. Click on the blue button to connect:

9. There you go, the k Drive content is displayed on the Finder:

### ... on Linux (Gnome)

To do this:

1. Open **Files.**
2. In the sidebar, click on **Network**:

3. Enter the **server address**: `davs://IDk Drive.connect.kdrive.infomaniak.com` (read the k Drive ID chapter above).
4. Click on **Connect**.
5. For the account settings, use the following information: Username: email address to log in to your Infomaniak account Password: create an application password for this specific use.
6. Click on **Login**.

### ... with a Windows software

Use the [Rai Drive](https://www.raidrive.com/) software for quick access to your hosted data. Complete the fields as in the image below:

### ... with a Windows / macOS software

Use the [Cyberduck](https://cyberduck.io/) software for quick access to your hosted data:

1. Open **Cyberduck**.
2. In the software menu, go to **Bookmark** then to **New bookmark**.
3. Select the **WebDAV (https)** protocol.
4. Provide the following information: Server address: https://IDk Drive.connect.kdrive.infomaniak.com (see the ID k Drive chapter above)Username: email address to log in to your Infomaniak account Password: create an application password for this specific use. Download folder: the folder where downloaded files will be stored

> **Note:** Most recent software supporting the WebDAV protocol is compatible with k Drive offers among those also supporting WebDAV. Infomaniak cannot guarantee the compatibility of the service with external applications and **does not provide support for this protocol**. It is recommended to [install the k Drive application](https://www.infomaniak.com/en/support/faq/2374) to avoid any file loss.

## Direct WebDAV connection URL to a specific folder

To facilitate a direct connection via WebDAV to a specific folder, you can use the following URL:

`https://IDk Drive.connect.kdrive.infomaniak.com/Common documents/Nom du dossier`

This simple method allows you to quickly access the desired folder without manually navigating the directory structure. Simply replace "`Folder name`" with the exact name of the target folder to establish a direct and secure connection via WebDAV. Also, refer to the last part of [this other guide](https://www.infomaniak.com/en/support/faq/2557) for other examples.