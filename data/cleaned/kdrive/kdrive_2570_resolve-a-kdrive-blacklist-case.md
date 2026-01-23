# Resolve a k Drive blacklist case

Source: https://www.infomaniak.com/en/support/faq/2570/resolve-a-kdrive-blacklist-case

---

This guide explains the **operation of the blacklist (***blacklisted***)** in the desktop app **k Drive** (macOS / Windows / Linux) and in which cases certain local files or folders are **no longer taken into account for synchronization**.

### Preamble

- A file or folder placed on the blacklist by the application has a **suffix in its name** of the form `_blacklisted`. This means that the application ignores this item during synchronization operations and are therefore not transferred to k Drive Web. This mark remains active as long as the cause of the block has not been corrected.
- If an **excluded** **folder** cannot be deleted locally, it can be automatically added to the blacklist. In this case, you can either delete it manually, or reactivate its synchronization in the application settings.
- Once the problem is resolved (for example after deleting a duplicate, correcting permissions, or reactivating an excluded folder), simply remove the suffix `_blacklisted` from the name of the item so that it is taken into account again in the synchronization.
- These mechanisms ensure the stability of the synchronization process and prevent repeated errors related to inaccessible, duplicate, or system-incompatible files.

## Examples of blacklisting

In some cases, a local item may be blacklisted:

- **Dehydrated placeholder (Lite Sync only)**: a *placeholder* file (not fully downloaded) is added to the blacklist to prevent it from being sent to k Drive Web.
- **Already existing creation on the remote drive**: if the creation of a file or folder fails because an identical item already exists on k Drive Web, the local item is marked as *blacklisted*.
- **Insufficient server-side permissions**: when a file or folder is created locally but the backend refuses to propagate it (for example in *Common documents*), the local item is blacklisted.
- **Folder excluded from synchronization**: if a folder has been unchecked in the k Drive desktop interface, the application attempts to delete it locally if it is still present. If this fails, it is blacklisted.

A blacklist can also occur due to **incompatible file names**: characters such as the tilde `~`, the slash `/`, the backslash `\`, certain system files such as `System Volume Information` or certain temporary or technical extensions (`.idlk`, `.parms.db`, `.directory`, `._*`, etc.).

Rename these items before restarting the synchronization.

## Correct an itemblacklisted

To recognize them:

- **Identification**: the suffix `_blacklisted` in the name of the file or folder indicates that the item is ignored by the synchronization.
- **Resolution**: correct the cause of the block (for example access permissions, an existing duplicate on k Drive Web, an exclusion parameter, or a placeholder status), then **rename** the item to remove `_blacklisted` if you want it to be synchronized again.

To avoid them:

- Check your **access rights** before creating or modifying files in shared spaces, organization folders, or *Common documents*.
- Avoid **duplicates** when creating or moving files between your computer and k Drive Web.
- Do not uncheck a folder in the desktop application if you continue to add items to it locally.
- With **Lite Sync**, download the file completely before modifying it instead of working on a dehydrated placeholder.