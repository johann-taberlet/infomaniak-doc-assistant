# Synchronize Joplin notes via WebDAV with k Drive

Source: https://www.infomaniak.com/en/support/faq/1800/synchronize-joplin-notes-via-webdav-with-kdrive

---

This guide explains how to store the *database* of Joplin on your [k Drive](https://infomaniak.com/gtl/kdrive) Infomaniak and connect your various devices via the `WebDAV` protocol. You thus keep your notes safe in a storage medium located in Switzerland.

**⚠ Available with:**

### Preamble

- [Joplin](https://joplinapp.org) is a free and open-source note-taking tool that allows you to organize all your notes within folders and access them from any device (computer, mobile device, etc.)
- Joplin will store several of its configuration files, so to avoid cluttering your k Drive directories, it is recommended to create a dedicated folder in your personal directory on k Drive, with a simple folder name like "`joplin`" for example, and then specify it at the end of the WebDAV link in step 7 below:

![image](https://faq.storage5.infomaniak.com/a7194e1a907f2a0def12ece6fd30e53fb31e591d.png)

## Configure Joplin to use k Drive via WebDAV

### Prerequisites

- Download [Joplin](https://joplinapp.org/download/)
- Know your [k Drive identifier](https://www.infomaniak.com/en/support/faq/2409) (*k Drive ID*).

The example below is substantially the same with all versions of Joplin:

1. Open the Joplin application.
2. Press the menu at the top left:

![sign](https://faq.storage.infomaniak.com/65b8eb1738ef42.19155028png)

3. Press **Settings**:

![sign](https://faq.storage.infomaniak.com/65b8eb61d380b2.13692573png)

4. Press **Synchronization.**
5. Press the menu to select a target.
6. Select the **WebDAV** mode:

![sign](https://faq.storage.infomaniak.com/65b8ec9481fe49.88077511png)

7. For the account parameters, use the following information: Server address: https://IDk Drive.connect.kdrive.infomaniak.com/joplin (or /folder-name — read the preamble above)Username: email address to log in to the Infomaniak user account Password: application password in case of double authentication activated or the one from your Infomaniak user account if you have not activated 2FA
8. Press the synchronization test and wait for the connection confirmation below:

![sign](https://faq.storage.infomaniak.com/65b8ed74e807b7.80170368png)

9. Press the top left to return to the previous menu and press **Synchronize** to create the files on k Drive:

![sign](https://faq.storage.infomaniak.com/65b8f125769279.98466075png)

10. Go back to the notes to start working.

> **Note:** ⚠️ The various services offered by Infomaniak are all compatible with the corresponding standard protocols (notably IMAP/SMTP for email, WebDAV for sharing, S3/Swift for storage, etc.). **Therefore, if you encounter a problem with third-party software, contact its publisher or a**[Partner](https://infomaniak.com/gtl/creez-votre-site.partners.create)**and consult the**[support policy](https://www.infomaniak.com/en/support/faq/2103) as well as article 11.9 of the [Infomaniak Terms and Conditions](http://infomaniak.com/gtl/rgpd.documents).