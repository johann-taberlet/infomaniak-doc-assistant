# Understanding kDrive permissions

Source: https://www.infomaniak.com/en/support/faq/2501/understanding-kdrive-permissions

---

This guide details the different assignments and access permissions for files/folders in [kDrive](https://infomaniak.com/gtl/kdrive) Infomaniak, including the restoration of inheritance of rights over the content of folders and subfolders.

### Preamble

- Refer to [this other guide](https://www.infomaniak.com/en/support/faq/2382) if you are looking for **general information** about sharing data on kDrive.
- Refer to [this other guide](https://www.infomaniak.com/en/support/faq/1793) for more specific information about sharing the **common** **folder**.
- Refer to [this other guide](https://www.infomaniak.com/en/support/faq/1633) regarding the more global permissions of users **within the Organization** if they are part of it.

## Types of access rights

A share (of a document, directory, etc.) on kDrive can be **restricted**. Choose whether the user…

- … can **view:**View onlyDownloadAdd a comment
- … can **modify:**Modify the fileDownloadAdd a commentAdd and create a file/folderDelete a file/folder
- … can **manage** (only if the share is within the common folder and not in a personal folder):Modify the fileDownloadAdd a commentAdd and create a file/folderDelete the fileShare with other usersManage user rights

The permissions granted as well as the information about the beneficiaries of the shares are visible on kDrive in the **column** “*Who has access*”:

![image](https://faq.storage5.infomaniak.com/34dab26b093e259d77f0b6e623e3c033deb67c42.gif)

An eventual public link activated on a file is indicated by a green icon in this column:

![image](https://faq.storage5.infomaniak.com/6c77fef19a76f9a8790e4c5d9332f28f8ac92beb.png)

## Assigning rights to the content of folders and subfolders

> **Note:** **The “Organization Folders” folder (common folder) does not necessarily mean that all kDrive users have access to it.**

Indeed, the share can be restricted and only part of the hierarchy can be shared with one or more users. Example of recursion when applying a share or removing it:

1. Imagine full access for all users to all the content of folders and subfolders.
2. If the share at the level of the **parent** folder (the folder at the very top of the hierarchy) is deleted, users will no longer have access to the content of the folders and subfolders.

### Resolving an inheritance rights issue

In the case where a **parent** folder is shared with multiple users, and subsequently, one of these users is removed from the share at one of the **child** folders (i.e., one of the subfolders of the main folder located higher in the hierarchy), then the day a new share with a collaborator is made at the level of the **parent** folder, **this share will not be propagated or inherited at the level of the child folders**.

1. A share is made with an additional user on a **parent** folder (*SEPT24*).The share is recursive over all the data contained in the child folders (assoc).
2. Sharing is removed from one of these **child** folders (*assoc*).
3. An additional share is made on the **parent** folder (*SEPT24*).The child folder does not inherit this share (due to the manual operation in point 2 above).
4. The solution is to click on the link present in the sharing window, which informs you of the incomplete share, which will restore the correct access rights according to the inheritance of the **parent** folder:

![image](https://faq.storage5.infomaniak.com/67527a6d957687f7be7f742b5887f212a5af95e2.png)