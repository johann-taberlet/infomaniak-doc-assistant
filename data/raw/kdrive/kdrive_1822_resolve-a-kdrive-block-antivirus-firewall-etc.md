# Resolve a kDrive block (antivirus, firewall, etc.)

Source: https://www.infomaniak.com/en/support/faq/1822/resolve-a-kdrive-block-antivirus-firewall-etc

---

This guide explains how to resolve an access or usage issue with [kDrive](https://infomaniak.com/kdrive) on Windows and macOS when third-party software can interfere with your synchronization.

> **Note:** If you notice a synchronization issue and missing folders, refer to [this other guide](https://www.infomaniak.com/en/support/faq/2153).

### Preamble

- The kDrive application may sometimes encounter interaction issues with Windows or macOS firewalls, as well as with software solutions for **antivirus, VPN**, or **cleaning**.
- This can result in the inability to synchronize files correctly or to use kDrive.
- In case of a problem, you must therefore manage to **authorize kDrive** within these applications and whitelist **at least two essential components**:kDrive.exe‍kDrive_client.exe‍

## Authorize kDrive on…

### … macOS

1. Open **System Preferences**
2. Click on **Security** or **Security** and **Privacy**
3. Select the **firewall**
4. Click the lock icon in the preferences pane and then enter an administrator name and password
5. Click the **Firewall Options** button
6. Click **Add an application (+)**
7. Select the applications (read the preamble) for which to authorize incoming connection privileges
8. Click **Add**
9. Click on **OK**

### ... Windows 10

1. Open the **Start menu**
2. Click on **Settings**
3. In the search field **Find a setting** type **Firewall**
4. Click on **Windows Firewall**
5. On the left click on **Allow an app or feature through Windows Firewall**
6. Now the windows Allowed apps will appear
7. Click on the button **Change settings**
8. **Check the boxes** next to the apps you want to allow through Windows Firewall (read the preamble)
9. Do not forget to also check the boxes under the **network type** that will allow this communication (private or public)
10. Click on **OK** to save your new settings

### ... Windows Defender

1. Open **Windows Defender** from the notification area
2. Select **Virus and threat protection**
3. Open **virus and threat protection settings**
4. Scroll down and select **Add or remove exclusions** in the **Exclusions** section
5. Click on **Add an exclusion**
6. Add the files (read the preamble)
7. Confirm the selection

### ... Avast

1. **Open** the Avast user interface **from the notification area**
2. Open **Settings**
3. Choose **General**
4. Open **Exclusions**
5. Click on **File Paths** then on **Browse**
6. Add the files (read the preamble)
7. Confirm the changes and enable real-time protection

### ... AVG

1. Refer to [this other guide](https://support.avg.com/SupportArticleView?urlname=avg-antivirus-scan-exclusions) by selecting the files (read the preamble) in step 5 to exclude kDrive

### … Avira

1. Right-click the **Avira** icon in the notification area and **disable real-time protection**
2. Expand **Avira** from the notification area
3. Click on **Add-ons**
4. Select **Settings** from the context menu
5. Open **PC protection** then **Scan**
6. Select **Exceptions** then **Add**
7. Add the files (read the preamble)
8. Go back to **PC protection** and expand **real-time protection**
9. Click on **Exceptions** then **Add**
10. Add the files (read the preamble)
11. Confirm the changes and enable real-time protection

### … Bitdefender

1. Refer to [this other guide](https://www.bitdefender.fr/consumer/support/answer/26042/) by selecting the files (read the preamble) in step 5 to exclude kDrive

### … CCleaner

1. In CCleaner, click on the **Options** icon
2. Click the **Exclude**
3. Click **Add**
4. Add the files (read the preamble)

### ... CleanMyMac

1. Click **View details** in the module analysis summary screen
2. Review the items displayed in the detailed results screen
3. Click the items to hide while holding down the Ctrl key
4. In the context menu, select **Add to exclusion list**
5. Add the files (read the preamble)

### ... ESET

1. **Open ESET** from the notification area
2. Press **F5** to open the **advanced configuration**
3. Open **Antivirus and antispyware**
4. Select **Exclusions**
5. Click **Add…** in the right pane
6. Add the files (read the preamble)
7. Confirm changes and reactivate real-time protection

### ... Kaspersky

To reduce problems related to the use of kDrive files when Kaspersky is installed, you can exclude kdrive.infomaniak.com from the analysis:

![image](https://faq.storage5.infomaniak.com/d446c6f3c79a74c7e9188163d6f40d72cc476c5e.png)

If the problem persists, uncheck the box (3) below:

![image](https://faq.storage5.infomaniak.com/ccf48e7950222d4088f769d52d72c269a9ac43b8.png)

### ... Malwarebytes

1. Open **Malwarebytes**
2. Select **Settings**
3. Choose **Malware Exclusions**
4. Click on **Add a file** to exclude a file
5. Add the files (read the preamble)
6. Confirm the selection and run the program

### ... McAfee

1. Refer to [this other guide](https://www.mcafee.com/support/?locale=fr-FR&articleId=TS102056&page=shell&shell=article-view) by selecting the files (read the preamble) to exclude kDrive.

### ... Norton

1. Refer to [this other guide](https://support.norton.com/sp/fr/fr/home/current/solutions/v3672136) by selecting the files (read the preamble) to exclude kDrive.

### ... NordVPN

Check within NordVPN and more specifically in [Anti-menaces Pro](https://nordvpn.com/features/threat-protection) (`Threat Protection`) the list of recent files supposed to be malicious in order to authorize the kDrive files.

> **Note:** ⚠️ For additional help [contact a partner](https://infomaniak.com/gtl/creez-votre-site.partners.annuaire) or [launch a free call for tenders](https://infomaniak.com/gtl/creez-votre-site.partners.create) — also discover the [role of the host](https://www.infomaniak.com/en/support/faq/2103).