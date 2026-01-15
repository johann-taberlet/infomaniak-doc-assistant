# Sync Synology with kDrive

Source: https://www.infomaniak.com/en/support/faq/2404/sync-synology-with-kdrive

---

This guide provides instructions to synchronize kDrive with a **Synology NAS** (or vice versa) via the `WebDAV` protocol found in the **Cloud Sync** application.

### Prerequisites

- Have a Synology NAS accessible from the Internet.
- Know your [kDrive identifier](https://www.infomaniak.com/en/support/faq/2409) (*kDrive ID*).

## Synchronize kDrive and Synology via Cloud Sync

To do this:

1. Log in to the Synology DiskStation Manager (DSM).
2. If necessary, download and install the **Cloud Sync** app from the **Package Center.**
3. Open **Cloud Sync.**
4. Click on the **+** at the bottom left to add a Cloud.
5. Choose **WebDAV** at the bottom of the list of available Clouds:

6. For the account parameters, use the following information:Server address: https://IDkDrive.connect.kdrive.infomaniak.com (see the prerequisites above)Username: email address to log in to the Infomaniak accountPassword: create an application password for this specific use.
7. Select the local folder, destination, and desired synchronization type:

Bidirectional: changes made will be reflected in both directions. Download only remote changes: ideal for saving a kDrive to your NAS. Download only local changes: ideal for saving data from your NAS to a kDrive.
