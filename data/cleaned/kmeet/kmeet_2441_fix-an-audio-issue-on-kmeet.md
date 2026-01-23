# Fix an audio issue on k Meet

Source: https://www.infomaniak.com/en/support/faq/2441/fix-an-audio-issue-on-kmeet

---

This guide helps you solve any **audio issues** with [k Meet](https://kmeet.infomaniak.com/), the ethical video conferencing solution offered by Infomaniak.

### Preamble

- With current security standards, a web browser or an application installed on an operating system like Windows or macOS will necessarily ask for your permission [to access thecamera](https://www.infomaniak.com/en/support/faq/2452) and the **microphone** as soon as a video conference begins.

## Tips to troubleshoot audio issues

### 1. (Re)authorize multimedia on computer

By going to the k Meet **Settings** (click on the icon  at the top right of the interface) you will (re)activate the requests for permission to access multimedia functions:

1. access to a microphone (choose the device that suits you)
2. access to the camera if available

Examples with the k Meet application on computer:

![image](https://faq.storage5.infomaniak.com/6e51cd43b39823f968abf8f17380300467502e8b.png)

![image](https://faq.storage5.infomaniak.com/4aedd1122ab87d2147398de238128b57104daf78.png)

Examples with the web version in your browser:

![image](https://faq.storage5.infomaniak.com/ad1345f1e85b626c6558e4d9990b24d42a06174b.png)

![image](https://faq.storage5.infomaniak.com/cd4163ed4463ad78bd4d7265170bc5f8d307c09a.png)

You can also check that a **lock** in your browser's address bar is not blocking your multimedia access by simply clicking on this lock.

### 2. Check multimedia on mobile device

If you have installed k Meet on [iOS](https://support.apple.com/fr-fr/guide/iphone/iph168c4bbd5/ios):

1. Go to Settings > Privacy & Security.
2. Tap on a hardware feature, such as 'Camera', 'Local Network', Bluetooth or 'Microphone'.
3. Check the settings related to k Meet in the list of apps.
4. Then, depending on your OS, go to Settings > Privacy and security > Security control.
5. Tap 'Manage shares and access', tap Continue, then follow the on-screen instructions to see if any setting might interfere with k Meet.

If you have installed k Meet on [Android](https://support.google.com/android/answer/9431959?hl=fr):

1. On your phone, open the **Settings.**
2. Tap on **Apps.**
3. Find **k Meet** or tap **Show all apps**, then select your application.
4. Tap on **Permissions.**
5. Tap on a permission setting to change it, then select **Allow.**

### 3. Windows Troubleshooter for audio issues

1. First, try accessing the **Windows settings** section **Privacy**.
2. Make sure the following access permissions are enabled: "Allow apps to access the camera" and “Choose which Microsoft Store apps can access the camera”.
3. Enable 'Windows Search', 'Camera' and 'App Connector'.
4. For the microphone, follow the same steps.

If that still doesn't work:

1. Go to **Search**  in the taskbar, type **Audio Troubleshooter**, then select **Find and fix problems playing sound** from the results to launch the troubleshooter.
2. Select **Next**, then select the device you want to troubleshoot, and proceed to the troubleshooter.

### 4. Join the ongoing meeting with a different device

If you encounter any audio/video issues during a k Meet meeting, join it from a different device. Were you on a **computer**? Use your **mobile device**! Or vice versa…

1. On the ongoing meeting with the device that is causing issues, invite a new participant to **get the meeting link**:

2. From a new device, open a **web browser** (Chrome, Safari, Firefox, etc.).
3. Enter the meeting link (*https://kmeet.infomaniak.com/* followed by the meeting link letters); example:

![sign](https://faq.storage.infomaniak.com/65e6e3374301e6.37827587png)

or proceed using the **code** of the meeting.

### 5. Disable WebRTC in Firefox

As a last resort, test [Firefox](https://mozilla.org) with WebRTC disabled to access your k Meet meeting:

1. Open Firefox.
2. Type in the Firefox address bar about:config
3. Find the parameter media.peerconnection.enabled; to avoid manual searching, you can type this parameter in the search box.
4. Set it to “false”.
5. Access the meeting via a link *kmeet.infomaniak.com* as indicated in chapter 4 above.