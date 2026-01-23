# Import data on k Drive via WebDAV

Source: https://www.infomaniak.com/en/support/faq/2557/import-data-on-kdrive-via-webdav

---

This guide explains how to **import external data (files, folders, etc.) into your**[k Drive](https://infomaniak.com/gtl/kdrive)**using the WebDAV protocol**.

### Preamble

- Refer to [this other guide](https://www.infomaniak.com/en/support/faq/1908) if you are looking for information on how to copy specific data from one k Drive to another when your user has access to both k Drives in question.
- Refer to [this other guide](https://www.infomaniak.com/en/support/faq/2409) if you are looking for information about using your k Drive via the WebDAV protocol in the future.

## Importing external data via WebDAV

### Prerequisites

- Have a [k Drive](https://infomaniak.com/gtl/ksuite.kdrive) or [k Suite](https://infomaniak.com/gtl/ksuite) subscription (WebDAV not required)
- Have sufficient permissions within [k Drive](https://www.infomaniak.com/en/support/faq/2365) or [k Suite](https://www.infomaniak.com/en/support/faq/879).
- **Do not change your password until the import is complete!**

To access the import tool, where the data needs to be imported:

1. [Click here](https://ksuite.infomaniak.com/kdrive) to access the Infomaniak **k Drive** web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. Click on the **Settings** icon  in the top right corner.
3. Check or select the relevant k Drive in the dropdown menu of the left sidebar.
4. Click on **General** in the left sidebar.
5. Click on **Import external data**:

6. Click the blue **Start** button:

7. Click on **WebDAV**.
8. Complete the requested information based on the source (including the WebDAV address you have - obtained from the source).
9. Choose the destination k Drive and the desired location to store the imported data.
10. Click on **Start**:

### Example: copying data from an external k Drive to the Organization

To import a k Drive that would be **outside the Organization in which your destination k Drive is located**, you need to enter the following information at point 9 above (your credentials will be used exclusively to import your data; they will be immediately deleted at the end of the process):

- **Username**: email address to log in to the Infomaniak account
- **Password**: create an [application password](https://www.infomaniak.com/en/support/faq/2855) for this specific use.
- **Entry point**: the WebDAV login URL with the **source k Drive ID** (starting disk) — refer to [this other guide](https://www.infomaniak.com/en/support/faq/2409) regarding the **k Drive ID**Example: https://123456.connect.kdrive.infomaniak.com if the ID is “123456” to obtain the entire k Drive; but it is also possible to import only a part (see below).

### Specify the name of a specific subfolder

It is possible to choose a subfolder as a **source folder**, by combining the [k Drive ID](https://www.infomaniak.com/en/support/faq/2409) and the folder path.

Example for a folder in the shared space of the **Organization Folders** (= "Common documents"):

- `https://IDk Drive.connect.kdrive.infomaniak.com/Common documents/Nom du dossier`

Example for a folder/subfolder that would be in the personal folders (therefore outside the *Organization Folders*):

- `https://IDk Drive.connect.kdrive.infomaniak.com/Nom du dossier/Nom du sous-dossier`