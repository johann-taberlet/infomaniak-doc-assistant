# RAG Quality Evaluation Report

**Generated:** 2026-01-16 20:26:27
**Questions Tested:** 20

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Score | 56/57 (98.2%) |
| Average Score | 2.95/3.00 |
| Average Coverage | 93.0% |
| Average Response Time | 17.0s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 18 | 94.7% |
| Partial (2) | 1 | 5.3% |
| Minimal (1) | 0 | 0.0% |
| Wrong (0) | 0 | 0.0% |

---

## Detailed Results

### kMeet (7 questions)

#### Q1: How do I create a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create a kMeet meeting, follow these steps:

### Prerequisites:
- You must have access to kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or the kMeet application for computers or mobile devices.

### Steps to Create a kMeet Meeting:
1. Start kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from the kMeet application.
2. Click the button to start a new meeting.
3. Enter a name for your meeting room.
4. Allow access to your webcam and microphone if prompted.
5. ...

**Key points found:** kmeet.infomaniak.com, enter meeting room name, allow webcam/microphone access, click Join the meeting, share room link

#### Q2: How can I share my screen during a kMeet call?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To share your screen during a kMeet call, follow these steps:

### Prerequisites
- You must have the **desktop** app kMeet (desktop application on macOS / Windows) or the **mobile** kMeet app (application for smartphone or tablet **Android**). The Web kMeet app (online service kmeet.infomaniak.com) is also compatible.
- Screen sharing is not yet possible with the mobile iOS app.
- If this is your first use or first screen share, the permissions requested by the operating system (macOS, Windows.....

**Key points found:** click screen icon with arrow, choose entire screen or specific window, not available on iOS, validate authorization, stop by clicking toolbar icon

#### Q3: What should I do if my audio is not working in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> If you are experiencing audio issues in kMeet, follow these troubleshooting steps:

### 1. (Re)authorize Multimedia Access
- Go to the kMeet **Settings** (click on the icon at the top right of the interface).
- Reactivate the requests for permission to access multimedia functions:
  - Access to a microphone (choose the device that suits you).
  - Access to the camera if available.
- Check that a **lock** in your browser's address bar is not blocking your multimedia access by clicking on the lock...

**Key points found:** check Settings for microphone permission, browser lock icon, mobile Privacy settings, Windows Audio Troubleshooter, try different device, Firefox WebRTC disable option

#### Q4: How do I create side rooms (breakout rooms) in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create side rooms (breakout rooms) in kMeet, follow these steps:

### Prerequisites:
- You must be a moderator of the meeting to create and manage side rooms.

### Steps to Create a Side Room:
1. Start kMeet as a moderator via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the applications for computer or mobile devices.
2. Once the participants are in the meeting, click on the multi-user icon in the kMeet toolbar.
3. Click the button to add a side room.
4. Participants c...

**Key points found:** must be moderator, click multi-user icon, add side room button, participants can join/leave, moderator can force participants to join

#### Q5: How can I record a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To record a kMeet meeting, follow these steps:

### Prerequisites:
- You must have a **kDrive** (standalone or as part of a kSuite).
- You must be the **moderator** of the video conference.
- The meeting must not be an **encrypted video conference with a custom key**.

### Steps to Record:
1. Start **kMeet** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the apps for computers and mobile devices.
2. Once in the meeting, click on the action menu **○○○** in the kMeet toolb...

**Key points found:** need kDrive, must be moderator, click action menu (three dots), Start recording, saved to kDrive root, .mp4 format, max 3 hours

#### Q6: How do I set a password for my kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To set a password for your kMeet meeting, follow these steps:

### Prerequisites:
- You must have access to kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or the kMeet application.

### Steps to Set a Password:
1. Start kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from the kMeet application.
2. Start a new meeting.
3. Enter a name for your meeting room.
4. Click on the security options.
5. Enable the toggle switch to **Protect access**.
6. Create the password...

**Key points found:** click security options, enable Protect access toggle, create password, share link AND password, end-to-end encryption option available

#### Q7: How can I livestream a kMeet meeting?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> To livestream a kMeet meeting, follow these steps:

### Prerequisites:
- You must be a **moderator** of the kMeet meeting to create a live broadcast link.
- It is **not necessary** to own an Infomaniak Video Streaming offer to use this feature.

### Steps to Livestream:
1. Start the kMeet meeting via [ksuite.infomaniak.com/kmeet](https://ksuite.infomaniak.com/kmeet) or from the kMeet application on your computer or mobile device.
2. Once in the meeting, click on the action menu (**○○○**) in the ...

**Key points found:** must be moderator, click action menu, Start live broadcast, copy stream URL to share, max 24 hours
**Key points missing:** stops when meeting ends

### kDrive (7 questions)

#### Q8: How do I install kDrive on Linux?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To install kDrive on Linux, follow these steps:

### Prerequisites:
- Ensure you have a Linux system that meets the requirements:
  - Officially supported systems: Ubuntu 22.04 LTS (or later) with GNOME or KDE desktop environments.
  - Infomaniak does not provide support for other Linux distributions or desktop environments.
- Download the kDrive desktop app for Linux (file type: .AppImage).
- Ensure you have the following dependencies installed:
  - Fuse2 (required to run AppImage):
    - For U...

**Key points found:** .AppImage file, install libfuse2, right-click Permissions, Allow executing file as program, Ubuntu 22.04 LTS officially supported, Lite Sync not available on Linux

#### Q9: How can I share a file from kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To share a file from kDrive, follow these steps:

### Prerequisites:
- You must have access to kDrive.

### Steps to Share a File or Folder:
1. Access the [kDrive Web app](https://ksuite.infomaniak.com/kdrive).
2. Right-click on the file or folder you want to share.
3. Click on **Share** at the top of the dropdown menu.

From there, you have two options:

#### Option 1: Create a Public Share Link
- Activate the **public share link**.
- Customize the sharing options:
  - Allow modifications (if t...

**Key points found:** right-click on file/folder, click Share, public share link option, can set expiration, password, add users with viewing/modification/management rights, recipients can create free Infomaniak account

#### Q10: What is a Drop Box in kDrive and how do I create one?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> A **Drop Box** in kDrive is a feature that allows you to create a designated folder where external contacts can upload files or folders directly into your kDrive. This is useful for collecting content from others without granting them full access to your kDrive. The files uploaded by your contacts are automatically organized in the specified location within your kDrive.

### How to Create a Drop Box in kDrive

To create a Drop Box in kDrive, follow these steps:

1. **Access kDrive**:
   - [Click...

**Key points found:** invite contacts to deposit files, click New then Drop Box, enter name, can set password, expiration, storage limit, email notification option, disable converts to regular folder

#### Q11: How do I resolve sync conflicts in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To resolve sync conflicts in kDrive, follow these steps:

### How to Display Conflicts
1. **Left-click** on the kDrive desktop app icon in your computer's notification area:
   - Top right on macOS
   - Bottom right on Windows
   - Double left-click in the taskbar on Linux
2. Click on the information button at the top.
3. Click on the listed event to view its details.
4. Conflicts and errors are displayed in two distinct tabs, allowing you to identify unsynchronized data.

### Resolving Conflict...

**Key points found:** conflicts when same file modified locally and online, kDrive Web version is kept, local saved as _conflict, can keep both, delete, or merge, view via kDrive icon > info, kDrive Rescue Folder for protection

#### Q12: How do I manage user rights in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To manage user rights in kDrive, follow these steps:

### Prerequisites:
- You must be an **Administrator** or **Legal Representative** within the Organization to manage user rights.
- The user must be added as a **collaborator** in the Organization.

### Steps to Manage User Rights:

1. **Access User Management:**
   - Go to the [Infomaniak Manager](https://manager.infomaniak.com/v3/ng/accounts/rights/users/list).
   - Click on the action menu **⋮** next to the user you want to manage.
   - Sel...

**Key points found:** Administrator vs User levels, Administrator has full access, User cannot manage product, Manage users in action menu, don't confuse Manager rights with kDrive rights

#### Q13: How can I access kDrive files locally without downloading them?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To access kDrive files locally without downloading them, you can use the **Lite Sync** feature on the kDrive desktop app for Windows or macOS. This feature allows you to virtually store your kDrive files on your computer, making them accessible without taking up local storage space. Here’s how it works:

### **Lite Sync Feature**
- **Purpose**: Saves space by storing files virtually on your computer. Files are only downloaded when you need to access them.
- **Accessibility**: Files are always ac...

**Key points found:** install kDrive desktop app, Open kDrive Web for server files, or open local folder, Lite Sync for virtual files
**Key points missing:** click icon in notification area

#### Q14: How do I sync kDrive with my Synology NAS?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To sync kDrive with your Synology NAS, follow these steps:

### Prerequisites:
- Have a Synology NAS accessible from the Internet.
- Know your kDrive identifier (kDrive ID).

### Steps to Sync kDrive and Synology via Cloud Sync:

1. Log in to the Synology DiskStation Manager (DSM).
2. If necessary, download and install the **Cloud Sync** app from the **Package Center**.
3. Open **Cloud Sync**.
4. Click on the **+** at the bottom left to add a Cloud.
5. Choose **WebDAV** at the bottom of the list...

**Key points found:** use Cloud Sync app, choose WebDAV, use application password, Bidirectional, Download remote, or Download local sync
**Key points missing:** server: https://[kDriveID].connect.kdrive.infomaniak.com

### kChat (5 questions)

#### Q15: How do I create a channel in kChat?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To create a channel in kChat, follow these steps:

### How to Create a Channel in kChat

1. Open the **kChat** web app (online service [ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat)).
2. Click on the **+** button located in the left sidebar.
3. Select **Create a new channel**.

### Information Related to a Channel

When creating a new channel, you can customize the following:

- **Name**: The name of the channel, which can be modified later.
- **URL**: By default, it uses the...

**Key points found:** click button in left sidebar, Create a new channel, set name, URL, private/public, description, General channel exists by default
**Key points missing:** can convert, leave, archive channels

#### Q16: What slash commands are available in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here are the details about slash commands in kChat:

### How to Use Slash Commands
To execute a slash command on kChat:
1. Click in the composition field within a channel.
2. Enter a `/` (slash or forward slash) followed by the command.
3. Confirm to send the command.

If you type only the `/` sign, a modal will appear displaying the available commands, such as going offline.

### Creating Custom Slash Commands
**Prerequisites:**
- You must not be an external user (external users will not see th...

**Key points found:** type / followed by command, just / shows available commands, can create custom slash commands, go to Integrations > Slash command, custom commands can call APIs, external users cannot access Integrations

#### Q17: How can I connect external applications to kChat?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> To connect external applications to kChat, you can use webhooks. Webhooks allow kChat to communicate with other applications or receive information from them to trigger actions within kChat. Here’s how you can set it up:

### Prerequisites:
- You must not be an external user (external users will not see the Integrations menu).

### Steps to Connect External Applications:
1. Access the **kChat** Web app by clicking [here](https://kchat.infomaniak.com/) or open the **kChat** desktop app (available...

**Key points found:** use webhooks, Integrations menu, Incoming webhooks receive from external apps, Outgoing webhooks send to external apps, external users cannot access Integrations
**Key points missing:** POST request with JSON text field

#### Q18: How do I translate a message in kChat?

**Rating:** [~] Partial (60.0% coverage)

**Response excerpt:**
> To translate a message in kChat, follow these steps:

1. Access the **kChat** web app by Infomaniak by clicking [here](https://ksuite.infomaniak.com/kchat) or open the mobile app (iOS/Android smartphone or tablet application) or the desktop app (macOS/Windows/Linux desktop application).
2. View the message you want to translate.
3. Click on the **action menu •••** located at the top right of the message.
4. Click on **Translate**.
5. The translated message will appear below your conversation and...

**Key points found:** click action menu (three dots) on message, click Translate, only visible to you
**Key points missing:** translation appears below, translates to your language

#### Q20: What is Euria and how do I use it in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> ### What is Euria and how do I use it in kChat?

**Euria** is an artificial intelligence integrated into **kSuite**, specifically designed to assist users within **kChat**. It can perform tasks such as calculations, translations, providing information, and answering questions. Euria is also capable of summarizing discussions in kChat, making it a powerful tool for productivity and collaboration.

---

### How to Use Euria in kChat

#### Add Euria to Your kChat Contacts
Euria is already available...

**Key points found:** Euria is AI assistant in kSuite, calculations, translations, information, search for bot in channel search, create private discussion with bot, do not create group conversation, new users get welcome message

---

## Recommendations

- **Good coverage achieved.** Focus on:
  - Response latency optimization
  - Edge case handling