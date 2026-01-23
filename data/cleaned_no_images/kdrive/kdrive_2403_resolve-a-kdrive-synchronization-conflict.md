# Resolve a k Drive synchronization conflict

Source: https://www.infomaniak.com/en/support/faq/2403/resolve-a-kdrive-synchronization-conflict

---

This guide details the possible solutions when the desktop app icon **k Drive** (desktop application on macOS / Windows / Linux) turns **orange**, which means there has been a **synchronization conflict**.

### Preamble

- k Drive does not indicate if a file is open or being modified on another local device (**no alert is displayed in this case**): It is therefore quite possible to view (read) a file while it is being modified on another device without this causing a conflict. The conflict only appears in case of simultaneous modification.

## k Drive synchronization conflict cases

### When do filesconflict?

- When you modify a file locally while it is also being modified on k Drive Web (the two versions become different).
- When you create or move a file while a similar operation is taking place simultaneously on k Drive Web.
- When you modify a file whose parent folder has been deleted on k Drive Web.
- When a file move cannot be synchronized correctly.

### In all these cases

- The k Drive Web version is kept as is.
- Your local version is saved as "[file name]_conflict".
- The conflicting file is not synchronized with k Drive Web.

### What to do with these filesconflict?

- Either keep both versions (but only the original file will synchronize).
- Either delete the `_conflict` file if it is the least recent version.
- Either delete the original version (not `_conflict`) if it is obsolete, then rename the `_conflict` to synchronize it.
- Either manually merge the two versions before deleting the `_conflict`.

### During a reinstallation of the k Drive application

These conflicts can also occur if you uninstall and then reinstall the application without deleting the configuration, while changes have been made on k Drive Web. To avoid this, it is recommended to:

- Either **do not keep the configuration** during uninstallation.
- Or fully synchronize **before** any uninstallation.
- Refer to the best practices further down in this guide.

## Managing synchronization conflicts

When **simultaneous modifications are made to the same file (locally and on k Drive Web, or while the application is closed)**, k Drive automatically manages these conflicts according to specific rules.

### For versions of the k Drive app prior to 3.6.11

- In case of simultaneous creation, concurrent modification, or conflicting movement, the k Drive Web version is always prioritized. The local version is renamed with “`_conflict`”.
- For conflicts involving deletion on the k Drive Web side, the local file is usually kept and resynchronized.
- Conflicting movements are canceled and recalculated based on the state of k Drive Web.

### From version 3.6.11 onwards

For files “*placeholder*” (files dehydrated via Lite Sync):

- They are automatically deleted locally.
- If the file still exists on k Drive Web, it is correctly resynchronized.

For other cases:

- The k Drive Web version remains prioritized in most situations.
- The conflicting local files are renamed with “`_conflict`”.
- Important exception: when a locally modified file should be deleted according to the state of k Drive Web…… it is moved to a folder named “k Drive Rescue Folder” (instead of being deleted); this protects your local modifications from accidental deletion.

Special cases:

- If a parent folder is deleted, locally modified files are preserved.
- Move cycles (mutually moved folders) are resolved in favor of the k Drive Web state.
- Rename conflicts prioritize the k Drive Web version.

## How to display conflicts?

To display conflicting files:

1. Perform a **left-click** on the desktop app icon **k Drive** in your computer's notification area (top right on macOS, bottom right on Windows and a double left-click in the taskbar on Linux).
2. Click on the information button at the top.
3. Click on the listed event to view its details:

4. Conflicts and errors are displayed in 2 distinct tabs allowing you to become aware of unsynchronized data:

5. **The first tab** allows you to resolve conflicts:

6. You will then need to choose how to resolve the conflict by deciding to send the local versionto the server (= synchronize)or to the computer's recycle bin

## Avoid synchronization conflicts

Recommendations:

- Do not work on the same file with multiple people (unless you are working online on a Word, Excel, or Power Point document).
- Synchronize your offline modifications before modifying the same files online.
- Avoid creating folders that have the same name as folders you do not synchronize on a device.

If necessary, to **manually resolve certain synchronization conflicts** that have not been resolved automatically:

1. **Open** both files.
2. **Compare** the differences.
3. **Retrieve** the information from the conflict file (the one with the exclamation mark) in the base file.
4. **Delete** the conflict file that is not synchronized (the one with the exclamation mark and the note `conflicted copy`):

**Don't see conflict files on all your devices?** That's normal; the conflict file (the one with the exclamation mark and the note `conflicted copy` in its name) is not synchronized. The idea is that you, the author of the changes, are the best person to resolve the conflict.

> **Note:** Refer to [this other guide](https://www.infomaniak.com/en/support/faq/2153) if you encounter a problem even though the **k Drive** desktop app icon is **green**.