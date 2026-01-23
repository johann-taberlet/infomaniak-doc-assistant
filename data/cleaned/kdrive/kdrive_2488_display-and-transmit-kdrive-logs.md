# Display and transmit k Drive logs

Source: https://www.infomaniak.com/en/support/faq/2488/display-and-transmit-kdrive-logs

---

This guide explains how to retrieve and transmit debugging information (logs, reports, and error logs) from the [k Drive](https://infomaniak.com/gtl/kdrive) application in case of a problem on macOS, Windows, or Linux.

**⚠ Available with:**

******Last 7 days only*

### Preamble

- For various reasons (a file type or a name length exceeding commonly accepted limits, etc.), it may happen that the synchronization by the k Drive app no longer progresses.
- Logs allow Infomaniak Support to better track the problem that may occur between your device and the k Drive application.
- The **extended logs** “record” k Drive activity from the moment you activate them; they are the ones that allow Infomaniak to trace the problem best.
- Refer to these other guides to try to resolve the issue without sending the logs: [conflicts](https://www.infomaniak.com/en/support/faq/2403) and [known issues](https://www.infomaniak.com/en/support/faq/2153).

## Save and Share Logs with Support

When requested by Infomaniak Support:

1. Open the k Drive application on your computer, **the app icon must be visible in the notification area**.
2. Perform a **left-click** on the app icon in the notification area of your computer (top right on macOS, bottom right on Windows, and a double left-click in the taskbar on Linux).
3. Click on the action menu **⋮** to the right of the application window.
4. Select **Application Preferences**:

5. Scroll down to the *Advanced* section and click the arrow to the right of the **debugging information**:

![image](https://faq.storage5.infomaniak.com/9e0702607c49ed869085a69d2c3c69f934992a21.png)

6. Check the box for **extended logs** as in the image below:

![image](https://faq.storage5.infomaniak.com/edafa9f2174ff1f90600fe3df752cd41def41a5e.png)

7. Click the **SAVE** button and **let the application run for at least 10 minutes**.
8. Return to the same place 10 minutes later (points 1-6 above) then **click the blue button to share** your debugging information with Infomaniak Support:

![image](https://faq.storage5.infomaniak.com/44b5de69f9f48ff35cde4d1a70aaf91c7edf418f.png)

9. Inform Infomaniak Support of this action within the ongoing exchange.

## Alternative method

If you encounter issues with the method above:

1. Click the blue link on the left to **Open the debug folder**.
2. From this folder, you will have access to all the bug reports of the k Drive application on your device:

![image](https://faq.storage5.infomaniak.com/c5a684234a8c4bace85052647ac0d12ebd7763e7.png)

If the application does not open, you can also access the logs through these paths:

- macOS: `/private/var/folders/h_/5c_k9rr564q0kzqv8rz8_dn80000gn/T/k Drive-logdir` (note `"h_/5c_k9rr564q0kzqv8rz8_dn80000gn"` will be different on your computer)

- Windows (copy-paste into the file explorer): `C:\Users\%USERNAME%\App Data\Local\Temp\k Drive-logdir` (if necessary, [enable hidden files and folders](https://support.microsoft.com/windows/voir-les-fichiers-et-les-dossiers-cach%C3%A9s-dans-windows-97fbc472-c603-9d90-91d0-1166d1d9f4b5) in the Windows Explorer)

- Linux: `/tmp/k Drive-logdir/`

To manually send the collected files:

1. If the files are **not large**, send them directly to Infomaniak Support within the ongoing exchange.
2. If the files are **large**, compress them in **.zip** format and send them to Infomaniak Support within the ongoing exchange.
3. If they are still too large to be sent by email, upload the .zip archive to [swisstransfer.com](https://swisstransfer.com) to obtain a **share link** that you will need to communicate to Infomaniak Support within the ongoing exchange:

![image](https://faq.storage5.infomaniak.com/007615405a7edd0c8af1954c82f36519224a7bba.png)