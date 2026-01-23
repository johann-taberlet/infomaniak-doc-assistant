# Sync Qnap with k Drive

Source: https://www.infomaniak.com/en/support/faq/2405/sync-qnap-with-kdrive

---

This guide provides instructions to synchronize [k Drive](https://infomaniak.com/gtl/kdrive) with a **Qnap NAS** (or vice versa) via the `WebDAV` protocol found in the **HBS 3 Hybrid Backup Sync** application.

**⚠ Available with:**

### Prerequisites

- Have a Qnap NAS accessible from the Internet.
- Know your [k Drive identifier](https://www.infomaniak.com/en/support/faq/2409) (*k Drive ID*).

## Synchronize k Drive and Qnap via HBS 3

To do this:

1. Log in to the Qnap NAS administration interface (QTS).
2. If necessary, download and install the app [HBS 3 Hybrid Backup Sync](https://www.qnap.com/en/software/hybrid-backup-sync).
3. Open **HBS 3.**
4. Go to **Sync** from the left menu.
5. Create a synchronization task (**Two-way Sync Job**).
6. Select **WebDAV** from the list of Cloud providers:

7. For the account parameters, use the following information:
 Server address: https://IDk Drive.connect.kdrive.infomaniak.com (see prerequisites above)Username: email address to log in to the Infomaniak account Password: create an application password for this specific use.
8. Select the local and destination folders:

9. Customize the task frequency.
10. Complete the wizard.