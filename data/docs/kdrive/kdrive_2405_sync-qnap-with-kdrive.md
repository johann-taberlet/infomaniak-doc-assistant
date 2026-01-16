# Sync Qnap with kDrive

Source: https://www.infomaniak.com/en/support/faq/2405/sync-qnap-with-kdrive

---

This guide provides instructions to synchronize [kDrive](https://infomaniak.com/gtl/kdrive) with a **Qnap NAS** (or vice versa) via the `WebDAV` protocol found in the **HBS 3 Hybrid Backup Sync** application.

**⚠ Available with:**

### Prerequisites

- Have a Qnap NAS accessible from the Internet.
- Know your [kDrive identifier](https://www.infomaniak.com/en/support/faq/2409) (*kDrive ID*).

## Synchronize kDrive and Qnap via HBS 3

To do this:

1. Log in to the Qnap NAS administration interface (QTS).
2. If necessary, download and install the app [HBS 3 Hybrid Backup Sync](https://www.qnap.com/en/software/hybrid-backup-sync).
3. Open **HBS 3.**
4. Go to **Sync** from the left menu.
5. Create a synchronization task (**Two-way Sync Job**).
6. Select **WebDAV** from the list of Cloud providers:

![image](https://faq.storage5.infomaniak.com/a8ebe352c85fd28de56f24eabf04521a5709eb0e.png)

7. For the account parameters, use the following information:
 Server address: https://IDkDrive.connect.kdrive.infomaniak.com (see prerequisites above)Username: email address to log in to the Infomaniak accountPassword: create an application password for this specific use.
8. Select the local and destination folders:

![image](https://faq.storage5.infomaniak.com/60abd07e6c6e1560b6ad4073a4d39f331e21b2ad.png)

9. Customize the task frequency.
10. Complete the wizard.