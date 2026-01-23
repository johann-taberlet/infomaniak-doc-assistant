# Resolve an editor block (kDrive iOS)

Source: https://www.infomaniak.com/en/support/faq/2892/resolve-an-editor-block-kdrive-ios

---

This guide explains how to resolve issues with opening the integrated document editor in the kDrive mobile app on iOS (iPhone / iPad).

### Preamble

- On iOS and iPadOS, the kDrive app uses a secure web view to launch the editor.
- If the device has active restrictions ("Screen Time" feature, parental controls, or MDM management), the operating system may block access to the technical URLs required by the editor.
- Unlike the Android version, which can use a third-party app installed, the iOS editor requires an active Internet connection; in the absence of a network, a message indicating the inability to open the editor will normally appear.

## Resolve a document editing access issue

If, when you try to edit a document (Word, Excel, PowerPoint) from the kDrive app on iOS:

- A message indicates: **Unable to load the document editor**,
- A blank page appears and remains stuck without an error message,
- The loading spins indefinitely after pressing the edit icon (pencil)…

… then it is necessary to specifically authorize Infomaniak domains in the iOS device settings:

1. Open the **Settings** of the iOS device.
2. Go to **Screen Time** > **Content & Privacy Restrictions**.
3. Enable restrictions if not already done, then tap **Content Restrictions** > **Web Content**.
4. In the **Always Allow** section, add the following two addresses:https://kdrive.infomaniak.comhttps://onlyoffice.infomaniak.com

Once these exceptions are added, go back to the kDrive app to relaunch the document editing.

> **Note:** For more details on configuring web restrictions on Apple devices, refer to the [official documentation](https://support.apple.com/fr-fr/HT201304#web-content).