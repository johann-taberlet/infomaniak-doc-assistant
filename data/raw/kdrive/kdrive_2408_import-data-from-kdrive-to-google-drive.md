# Import data from kDrive to Google Drive

Source: https://www.infomaniak.com/en/support/faq/2408/import-data-from-kdrive-to-google-drive

---

This guide details how to import **Google Drive** data using **rClone** on [kDrive](https://infomaniak.com/gtl/kdrive) Infomaniak.

**⚠ Available with:**

## 1. Configure rclone for drive access

### Install rclone on your computer

There is a version of *rclone* with a graphical interface ([GUI](https://rclone.org/gui/)) but it is quite possible to do this via the command line (CLI):

1. Install *rclone* from a `Terminal` type application on your device by typing the entire following command:
`sudo -v ; curl https://rclone.org/install.sh | sudo bash`
2. Enter the password for your session on your computer to start the installation:

![image](https://faq.storage5.infomaniak.com/057eab83b978cc2c211fb6e87581b5f007abc083.png)
Refer to the official installation guide if necessary.

### Configure the remote disk (Google Drive) on rclone

1. Once *rclone* is installed, enter the command `rclone config`.Refer to the official configuration guide if necessary.
2. Then choose to configure a new remote import by answering `n` for `New remote`.
3. Name the remote disk, for example `gdrive`:

![image](https://faq.storage5.infomaniak.com/539fa24f75731eef3063e0107f27daa2bb0c6a92.png)

4. Then choose the type of disk to import by answering `drive` which corresponds to **Google Drive** among the proposed choices.

You must then authorize the connection to Google Drive from a browser.

> **Note:** By default, *rclone* uses a shared client ID among all users, which may result in request limitations imposed by Google. It is strongly recommended to use your own client ID to avoid these restrictions.

1. **Access the**[Google API Console](https://console.developers.google.com/) with your Google account.
2. **Create or select a project.**
3. **Enable the Google Drive API** via the button/link "Enable APIs and Services".
4. Search for the keyword `Drive` and click on `Google Drive API`:

![image](https://faq.storage5.infomaniak.com/8700f387c9af90fe9a360da3bb31278a436711c1.png)

5. Click on the **Enable** button.
6. Click on **Credentials** in the left sidebar (and not on a similar button).
7. Click on **Configure the OAuth consent screen** (if not already done):Enter a name, for example rclone.Select "External" (or "Internal" if you are a Google Workspace user).Under “Data Access”, add the scopes ("fields of application") required:https://www.googleapis.com/auth/docs,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/drive.metadata.readonlySave.Add your email account as a test user under "Audience".Return to the "Google Auth Platform" section.
8. **Create OAuth credentials**:Click on "Create credentials / OAuth client ID".Choose "Desktop app" and leave the default name, then click on the Create button.Keep the client ID and the client secret code displayed.
9. **If "External" was chosen in step 7 above**, return to "**Audience**" in the left sidebar and click on "**Publish the application**".

> **Note:** Due to the "enhanced security" recently introduced by Google, you are theoretically supposed to "submit your application for verification" and wait several weeks for their response.
In practice, you can directly use the client ID and client secret with rclone (read the rest of the guide). The only consequence will be a very intimidating confirmation screen when you log in via your browser to allow rclone to obtain its token-id. However, since this only happens during the initial setup of the remote storage, it is not a major issue.
It is also possible to leave the application in "Test" mode, but in this case, any authorization will expire after a week, which can be cumbersome to renew frequently. If a short validity period does not pose a problem for your use, then keeping the application in test mode may be sufficient.

Return to *rclone*in the terminal:

1. Indicate to *rclone* the `client_id` by copying-pasting the `Client ID` obtained in step 8 above, same for the secret phrase.
2. Then choose the `scope` n°1:

![image](https://faq.storage5.infomaniak.com/ac848bd17b9c8592047f3994f88e6df5efb7cd8d.png)

3. Press the “`Enter`” key to leave the `service_account_file`. question blank
4. Answer “No” `n` to the question about “advanced configuration”.
5. Answer “Yes” `y` to the question about the web browser connection:

![image](https://faq.storage5.infomaniak.com/a12324deda42612b1631a979e5cb8ef0dda07e87.png)

6. A web page opens in your web browser allowing you to connect to Google and authorize the application you created in step 9 above.
7. Once permissions are granted, you should receive the following message:

![image](https://faq.storage5.infomaniak.com/5a2126de55dd9d76c5656ab662e42191c30f7c20.png)

8. In the terminal, answer “No” `n` to the question about “`Shared Drive (Team Drive)`”.
9. Answer “Yes” `y` to the last question:

![image](https://faq.storage5.infomaniak.com/d8db20c5969a8df1d470fec8102e571b455fcc60.png)

### Configuration of the destination disk (kDrive) on rclone

It is possible to act directly on [the configuration file ofrclone](https://rclone.org/commands/rclone_config_file/) by pasting your kDrive configuration in it, for example:

```
[kdrive]
type = webdav
url = https://kDrive_ID_HERE.connect.kdrive.infomaniak.com/
vendor = other
user = user@email.com
pass = PASSWORD_HERE_OR_APP_PASSWORD_IF_2FA
```

But here is how to proceed step by step as for the previous configuration:

1. Still in the terminal, enter `n` for a new disk configuration and enter the name `kDrive` to recognize your destination disk:

![image](https://faq.storage5.infomaniak.com/bae2707f23e257c1ad9cd8e20a4b9ddf90fed124.png)

2. Then choose the type of disk to import by answering `webdav` which corresponds to a WebDAV configuration among the choices offered.
3. Enter the following information:url = direct access to kDrive (refer to this other guide regarding the kDrive ID for the connection URL)vendor = rclone (option number 6)user = email address to log in to the Infomaniak user account
4. Answer “Yes” `y` to the question about the password, then enter the password:application password in case of double authentication activated or the one of your Infomaniak user account if you have not activated 2FA.
5. Leave `bearer_token` blank, then answer “No” `n` to the question about “advanced configuration”.
6. Answer “Yes” `y` to the last question and your 2 disks are displayed:

![image](https://faq.storage5.infomaniak.com/8a2a9718f49dfeaee411a895c30c92163740afda.png)

## 2. Copy data from Google Drive to kDrive

> **Note:** kDrive supports [rclone streaming upload](https://rclone.org/overview/#optional-features) via WebDAV, up to 50 GB (extendable to 100 GB) to avoid abuse, with automatic error handling if the limit is exceeded without prior specification of the size via `Content-Length`.

### Prerequisites

- Consult the available options in the [official guide](https://rclone.org/drive/) before starting an import, particularly these important commands:--drive-skip-shortcuts to avoid infinite import loops--drive-shared-with-me to get what has been shared--drive-acknowledge-abuse to force the download of files blocked by Google

Example of a command to start copying your Google Drive to the root of your kDrive:

```
sudo rclone copy gdrive: kDrive:
```

This will immediately start copying your folders, subfolders, and Google Drive contents to the **personal folder** of your Infomaniak kDrive!

> **Note:** **Google documents** such as Gdocs, Sheets, Slides, etc. are converted to Office formats like `.docx`, `.xlsx`, etc. and are readable directly on kDrive.