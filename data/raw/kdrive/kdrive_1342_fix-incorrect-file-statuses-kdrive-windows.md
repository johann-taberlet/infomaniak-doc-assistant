# Fix incorrect file statuses (kDrive Windows)

Source: https://www.infomaniak.com/en/support/faq/1342/fix-incorrect-file-statuses-kdrive-windows

---

This guide helps resolve an issue with statuses (`OK`, `in progress`, etc.) that may occur with the files and folders in the kDrive tree in Windows Explorer, in case these indications no longer match reality.

## Resolve the issue of incorrect statuses

The problem is visible in the kDrive log as follows:

```
20240616_2008_kDrive.log:2024-06-16 20:19:01:349 [I] (6732) socketlistener.cpp:46 - Sending SocketAPI message --> STATUS:OK:D:\kDrive\Photos\Personnal\2024\06_June\0616_Bern\HP7A6181.JPG to 0000025197E46A60
```

The application sends the correct file status to the explorer, for example, the status sent here is `OK`, the status icon displayed should be the green circle, but the displayed status does not match:

![image](https://faq.storage5.infomaniak.com/1edde450fc35109cef8d7b880c3fc0d81488787b.png)

### Restart Windows Explorer

To do this:

1. Access the task manager by pressing `ctrl shift + esc`.
2. In the task manager, search for Windows Explorer.
3. Right-click on it and click on **End Task**.
4. In the upper left corner of the task manager, click on **File**.
5. Click on **Run a new task**.
6. Type: `explorer.exe`.
7. Press **Enter**.

### Check and repair system integrity

To do this:

1. Open the command prompt with administrator access.
2. Type each command below and wait for the analysis to complete:

```
SFC /scannow
DISM /Online /Cleanup-Image /CheckHealth
DISM /Online /Cleanup-Image /ScanHealth
DISM /Online /Cleanup-Image /RestoreHealth
```