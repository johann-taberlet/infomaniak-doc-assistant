# Manage kDrive file deletion

Source: https://www.infomaniak.com/en/support/faq/2383/manage-kdrive-file-deletion

---

This guide explains how to manage the behavior of deleted files and the trash of [kDrive](https://infomaniak.com/gtl/kdrive).

### Preamble

- When a file is deleted from one of the tools synchronized with kDrive, the kDrive Web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) moves the file to its trash.
- If this kDrive trash is emptied, **it is impossible to recover its contents**.
- If the trash of the operating system of the computer on which kDrive is installed is emptied, this does not empty the trash of the kDrive Web app **kDrive**.
- The file remains **for a minimum of 30 days** after it arrives in the kDrive trash, but some offers can define a retention period of up to 365 days:

**⚠  Maximum duration that can be chosen for the retention of files in the kDrive trash:**

## Organize the trash…

### … of the kDrive Web app

To access the trash files:

1. [Click here](https://manager.infomaniak.com/v3/ng/products/ksuite/kdrive) to access the management of your product on the Infomaniak Manager ([need help?](https://www.infomaniak.com/en/support/faq/1990#nav)).
2. Click directly on**the name** assigned to the product concerned.
3. Click on **Trash** in the left sidebar to view the files that are in it.
4. Click on **Settings** to configure the retention duration of files in the trash:

![image](https://faq.storage5.infomaniak.com/70a4359ccc6b2bd305d13c9327446ef1bd9b92a5.png)

5. Choose the desired duration from the dropdown menu (3 months, 6 months, 1 year).
6. Confirm the settings by clicking the **Confirm** button:

![image](https://faq.storage5.infomaniak.com/cd16e6b0db3e31ce391ac38a0d3f2d25ae750d05.png)
You can also access it by clicking on the Settings icon ‍ at the top right of the interface (point 3 in the image above) then on Trash Settings in the left sidebar (point 4).

### … of the kDrive desktop app

To choose whether deleting a file on the Web app or the mobile app should place the file synchronized with the desktop app in the computer's trash:

1. Left-click on the desktop app icon in the notification area of your computer (top right on macOS, bottom right on Windows and a double left-click in the taskbar on Linux).
2. Click on the action menu **⋮** on the right of the window that appears.
3. Click on **Application Preferences**:

![image](https://faq.storage5.infomaniak.com/6624aaaf9c27bbebd9d790fa666a20db538faba9.png)

4. Enable or disable the toggle switch to decide whether to send the synchronized version to the computer's trash:

![image](https://faq.storage5.infomaniak.com/9be360d2e7d09a6d27d4705727c0eded4cef94f1.png)

### Resolve a trash problem on computer

In rare cases, it may happen that despite a setting to move files to the trash (point 4 above), the desktop app permanently deletes the file erased from:

- … the Web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive))…
- … the mobile app (application for iOS / Android smartphone or tablet)…
- … another synchronized computer…

instead of placing it in the trash, because:

- **Insufficient space**: the trash has reached its maximum configured size.
- **No trash**: on some file systems, such as network or removable drives (USB key for example), there may be no trash.

This list is not exhaustive but it covers the majority of cases that will not be reported to the user. Other issues such as those related to the use of disks mounted as read-only will be taken into account and reported to the user.

## Restore a file from the trash…

### … on the kDrive Web app

To **restore** a file to its original location **when the trash has not yet been emptied**:

1. [Click here](https://manager.infomaniak.com/v3/ng/products/ksuite/kdrive) to access the management of your product on the Infomaniak Manager ([need help?](https://www.infomaniak.com/en/support/faq/1990#nav)).
2. Click directly on**the name** assigned to the product concerned.
3. Click on **Trash** in the left sidebar.
4. Select the items to restore.
5. Click on **Restore:**

 

You can restore the file to a **location of your choice** or to its **original location**.

To restore an entire kDrive as it was before file moves or reorganizations, refer to [this other guide](https://www.infomaniak.com/en/support/faq/1838).

To restore a **previous version** of an existing file, refer to [this other guide](https://www.infomaniak.com/en/support/faq/2384).