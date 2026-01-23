# Resolve an issue accessing folders (k Drive Windows)

Source: https://www.infomaniak.com/en/support/faq/1686/resolve-an-issue-accessing-folders-kdrive-windows

---

This guide helps you regain control of a folder present on the Windows operating system in certain problematic cases of [k Drive](https://infomaniak.com/kdrive). This scenario is common for **system folders** belonging to the `Trusted Installer` group.

> **Note:** If you encounter a display or access error to k Drive or one of the folders, refer to [this other guide](https://www.infomaniak.com/en/support/faq/1822).

## Taking ownership of a folder

Here's how to regain possession of such a folder:

1. Right-click on the folder in question.
2. Select **Properties**.
3. Go to the **Security** tab.
4. Click on the **Advanced** button at the bottom of the window.
5. Click on **Change** next to the **Owner** field.
6. Click on **Advanced**.
7. Click on **Find Now**.
8. Select your user account from the list and click on **OK**.
9. Click **OK** again, the folder owner has been modified.
10. Check the 2 boxes **Replace owner on subcontainers and objects** to take ownership of the files and subfolders of this folder:

11. Click on **OK** to validate.