# Sync Synology with k Drive

Source: https://www.infomaniak.com/en/support/faq/2404/sync-synology-with-kdrive

---

This guide provides instructions to synchronize [k Drive](https://infomaniak.com/gtl/kdrive) with a **Synology NAS** (or vice versa) via the `WebDAV` protocol found in the **Cloud Sync** application.

**⚠ Available with:**

### Prerequisites

- Have a Synology NAS accessible from the Internet.
- Know your [k Drive identifier](https://www.infomaniak.com/en/support/faq/2409) (*k Drive ID*).

## Synchronize k Drive and Synology via Cloud Sync

To do this:

1. Log in to the Synology Disk Station Manager (DSM).
2. If necessary, download and install the **Cloud Sync** app from the **Package Center.**
3. Open **Cloud Sync.**
4. Click on the **+** at the bottom left to add a Cloud.
5. Choose **WebDAV** at the bottom of the list of available Clouds:

![image](https://faq.storage5.infomaniak.com/1965517315e78a34bdc9376b1d83aeec127eadc9.png)

6. For the account parameters, use the following information: Server address: https://IDk Drive.connect.kdrive.infomaniak.com (see the prerequisites above)Username: email address to log in to the Infomaniak account Password: create an application password for this specific use.
7. Select the local folder, destination, and desired synchronization type:

![image](https://faq.storage5.infomaniak.com/a4fae69d74d2fc186771d48ed16bbf86d0bd170a.png)
Bidirectional: changes made will be reflected in both directions. Download only remote changes: ideal for saving a k Drive to your NAS. Download only local changes: ideal for saving data from your NAS to a k Drive.