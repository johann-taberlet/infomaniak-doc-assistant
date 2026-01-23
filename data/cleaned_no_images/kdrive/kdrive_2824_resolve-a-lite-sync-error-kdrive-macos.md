# Resolve a Lite Sync error (k Drive macOS)

Source: https://www.infomaniak.com/en/support/faq/2824/resolve-a-lite-sync-error-kdrive-macos

---

This guide explains how to resolve certain **Lite Sync macOS** errors that may occur with the desktop app [k Drive](https://infomaniak.com/gtl/kdrive) (desktop application on macOS).

## Sync lock 1/10

Check if macOS permissions are enabled for k Drive and Lite Sync extensions:

1. Open macOS settings.
2. Under **General**, click on **Open and extensions.**
3. Scroll down to the **Endpoint Security Extensions :: k Drive Lite Sync Extension**:

4. Check that the permissions are enabled and validate at the bottom:

Take the opportunity to check the other elements related to k Drive to ensure that everything is enabled.

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
* * 864VDCS2QY com.infomaniak.drive.desktopclient. Lite Sync Ext (3.5.0/1) k Drive Lite Sync Extension [activated enabled]
```

If the command result does not mention "`k Drive Lite Sync Extension`", the extension is not present:

- Delete the sync and add it again.

If the command result does not have the status `[activated enabled]`:

- Authorize the extension in the *System Settings / Privacy and Security.*

### ... check the extension permissions

In the *System Settings / Privacy and Security / Full Disk Access* of the macOS device:

Grant full access to **k Drive** and the **Lite Sync** extensions:

### ... check the extension's operation

From a Terminal:

```
% ps -ef | grep Lite Sync Ext
```

The result is similar to:

```
0  7434     1   0  1:02   ??         0:25.42 /Library/System Extensions/6035BDE4-B7D6-477E-A6AB-C2281E3C7752/com.infomaniak.drive.desktopclient. Lite Sync Ext.systemextension/Contents/MacOS/com.infomaniak.drive.desktopclient. Lite Sync Ext
```

If the extension does not seem to be working, try the following actions:

- Restart the app.
- Reboot the Mac.
- Remove/add the sync.
- Uninstall/reinstall the app.

### If it is still not OK

- Request [k Drive logs](https://www.infomaniak.com/en/support/faq/2488) (level **Debug**):

- Check in the **Console** for any blockage reports on the date of the last app startup and, if so, send them to Infomaniak:

Retrieve k Drive messages in the Console:

- Quit the app.
- In the **Console**, select the Mac, filter on `[KD]`, click on Start:

- Launch the app.
- Click in the list of messages, select them (Ctrl+A), copy them (Ctrl+C) and send them to Infomaniak.