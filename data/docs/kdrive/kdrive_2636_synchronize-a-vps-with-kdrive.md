# Synchronize a VPS with kDrive

Source: https://www.infomaniak.com/en/support/faq/2636/synchronize-a-vps-with-kdrive

---

This guide provides instructions to synchronize [kDrive](https://infomaniak.com/gtl/kdrive) with a VPS (or vice versa) via the `WebDAV` protocol found in the **rClone** application.

**⚠ Available with:**

### Prerequisites

- Have a VPS.
- Know your [kDrive identifier](https://www.infomaniak.com/en/support/faq/2409) (*kDrive ID*).

## Synchronize kDrive and VPS via rClone

This operation allows you to retrieve in real-time the files and folders from kDrive and to read, create, or modify these files from your VPS while ensuring they are synchronized back to the kDrive server. An rClone mount point can be created with a folder on your VPS to manipulate these kDrive files.

Refer to the [rClone documentation](https://rclone.org/commands/rclone_mount/) if you are looking for information about the available options:

1. Example of an rClone command:rclone mount kdrive:/My_kDrive_Folder_Path /home/ubuntu/Target_Folder_Path --vfs-cache-mode full --vfs-cache-max-age 24h --vfs-cache-max-size 10G --cache-dir /home/ubuntu/rclone/cache --daemon --allow-other --dir-cache-time 1h --log-file /home/ubuntu/rclone/rclone.log --log-level INFOThe --daemon attribute of this command allows you to run the synchronization as a background task because without it, the sync stops at each VPS disconnection…
2. Example of an rClone configuration file:[kdrive]
type = webdav
url = https://***.connect.kdrive.infomaniak.com/***
vendor = other
user = ***
pass = ***Server address: https://IDkDrive.connect.kdrive.infomaniak.com (refer to the prerequisites above)Username: email address used to log in to your Infomaniak accountPassword: create an application password for this specific use.