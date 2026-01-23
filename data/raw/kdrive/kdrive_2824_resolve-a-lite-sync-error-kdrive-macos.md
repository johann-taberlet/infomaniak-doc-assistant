# Resolve a Lite Sync error (kDrive macOS)

Source: https://www.infomaniak.com/en/support/faq/2824/resolve-a-lite-sync-error-kdrive-macos

---

This guide explains how to resolve certain **Lite Sync macOS** errors that may occur with the desktop app [kDrive](https://infomaniak.com/gtl/kdrive) (desktop application on macOS).

## Sync lock 1/10

Check if macOS permissions are enabled for kDrive and Lite Sync extensions:

1. Open macOS settings.
2. Under **General**, click on **Open and extensions.**
3. Scroll down to the **Endpoint Security Extensions :: kDrive LiteSync Extension**:

![image](https://faq.storage5.infomaniak.com/bc223f1b60a738b6b86aa0d913686a48db53e8cd.png)

4. Check that the permissions are enabled and validate at the bottom:

![image](https://faq.storage5.infomaniak.com/6de6ae0387de1d9e81e90ac5b8455bdefeb923c3.png)

Take the opportunity to check the other elements related to kDrive to ensure that everything is enabled.

## Error of type "Unable to start Lite Sync plugin"

To correct an error of type "`Unable to start Lite Sync plugin`" which usually occurs when the [Lite Sync](https://www.infomaniak.com/en/support/faq/2608) extension has disappeared or does not have the necessary permissions…

### ... check the presence of the extension

From an application of type `Terminal` (command line interface, `CLI / Command Line Interface`) on a macOS device:

```
% systemextensionsctl list
```

The result is similar to:

```
1 extension(s)
--- com.apple.system_extension.endpoint_security
enabled active teamID bundleID (version) name [state]
* * 864VDCS2QY com.infomaniak.drive.desktopclient.LiteSyncExt (3.5.0/1) kDrive LiteSync Extension [activated enabled]
```

If the command result does not mention "`kDrive LiteSync Extension`", the extension is not present:

- Delete the sync and add it again.

If the command result does not have the status `[activated enabled]`:

- Authorize the extension in the *System Settings / Privacy and Security.*

### ... check the extension permissions

In the *System Settings / Privacy and Security / Full Disk Access* of the macOS device:

![image](https://faq.storage5.infomaniak.com/ea89ba3bd8535baec03180ad167c8c47ab3d93fa.png)

Grant full access to **kDrive** and the **Lite Sync** extensions:

![image](https://faq.storage5.infomaniak.com/9c22c56d498db09110c4efa928064a8384374e57.png)

### ... check the extension's operation

From a Terminal:

```
% ps -ef | grep LiteSyncExt
```

The result is similar to:

```
0  7434     1   0  1:02   ??         0:25.42 /Library/SystemExtensions/6035BDE4-B7D6-477E-A6AB-C2281E3C7752/com.infomaniak.drive.desktopclient.LiteSyncExt.systemextension/Contents/MacOS/com.infomaniak.drive.desktopclient.LiteSyncExt
```

If the extension does not seem to be working, try the following actions:

- Restart the app.
- Reboot the Mac.
- Remove/add the sync.
- Uninstall/reinstall the app.

### If it is still not OK

- Request [kDrive logs](https://www.infomaniak.com/en/support/faq/2488) (level **Debug**):

![image](https://faq.storage5.infomaniak.com/ed0c7005374d4c05a8ed2a85dfdc52ea8bcde2b9.png)

- Check in the **Console** for any blockage reports on the date of the last app startup and, if so, send them to Infomaniak:

![image](https://faq.storage5.infomaniak.com/14b7947b393a4e931f3896f0ec8942c97b1926d9.png)

Retrieve kDrive messages in the Console:

- Quit the app.
- In the **Console**, select the Mac, filter on `[KD]`, click on Start:

![image](https://faq.storage5.infomaniak.com/d66cc510ad6fd7ea027d5c830a403fde0e6c6467.png)

- Launch the app.
- Click in the list of messages, select them (Ctrl+A), copy them (Ctrl+C) and send them to Infomaniak.