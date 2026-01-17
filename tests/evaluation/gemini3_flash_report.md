# RAG Quality Evaluation Report

**Generated:** 2026-01-16 21:32:34
**Questions Tested:** 20

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Score | 60/60 (100.0%) |
| Average Score | 3.00/3.00 |
| Average Coverage | 96.3% |
| Average Response Time | 7.4s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 20 | 100.0% |
| Partial (2) | 0 | 0.0% |
| Minimal (1) | 0 | 0.0% |
| Wrong (0) | 0 | 0.0% |

---

## Detailed Results

### kMeet (7 questions)

#### Q1: How do I create a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create a kMeet meeting, you can use the instant method via a browser/app or schedule it through the Infomaniak Calendar.

### Instant Meeting Creation
1. **Access kMeet**: Go to [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or use the computer or mobile application.
2. **Start Meeting**: Click on **Start a new meeting**.
3. **Name the Room**: Enter a name for your meeting room so participants know the subject.
4. **Permissions**: Allow access to your webcam and microphone when prompted...

**Key points found:** kmeet.infomaniak.com, enter meeting room name, allow webcam/microphone access, click Join the meeting, share room link

#### Q2: How can I share my screen during a kMeet call?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To share your screen during a kMeet call, follow these steps and take note of the platform-specific requirements.

### How to start screen sharing
1. Start kMeet via the [web interface](https://kmeet.infomaniak.com), the desktop application (Windows, macOS, Linux), or the mobile app (Android).
2. Create or join a meeting room.
3. Click on the **screen icon with an arrow** ("Share your screen") in the bottom toolbar.
4. Read and validate any authorization warnings displayed by your device.
5. Cho...

**Key points found:** click screen icon with arrow, choose entire screen or specific window, not available on iOS, validate authorization, stop by clicking toolbar icon

#### Q3: What should I do if my audio is not working in kMeet?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> If you are experiencing audio issues in kMeet, follow these troubleshooting steps based on your platform:

### 1. (Re)authorize Multimedia Access
Modern browsers and operating systems require explicit permission to access your microphone.
*   **On Computer (Web or App):** Go to the kMeet **Settings** (gear icon at the top right) to reactivate permission requests. You can also select the specific microphone device you wish to use here.
*   **Browser Lock Icon:** Click the **lock icon** in your br...

**Key points found:** check Settings for microphone permission, browser lock icon, mobile Privacy settings, Windows Audio Troubleshooter, try different device
**Key points missing:** Firefox WebRTC disable option

#### Q4: How do I create side rooms (breakout rooms) in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> In kMeet, side rooms (also known as breakout rooms) allow you to divide a main meeting into several simultaneous discussions in distinct virtual spaces.

### Prerequisites & User Roles
*   **Moderator Role Required:** Only a [moderator](https://www.infomaniak.com/en/support/faq/2476) can create side rooms and manage participant movement between the main room and subgroups.
*   **Platform Availability:** This feature is available via the web ([kmeet.infomaniak.com](https://kmeet.infomaniak.com)) ...

**Key points found:** must be moderator, click multi-user icon, add side room button, participants can join/leave, moderator can force participants to join

#### Q5: How can I record a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To record a kMeet meeting, follow these steps and requirements:

### Prerequisites
*   **kDrive access:** You must have an active kDrive (either standalone or as part of a kSuite).
*   **Moderator role:** You must be the moderator of the video conference to start the recording.
*   **No custom encryption:** You cannot record if the meeting was created as an [encrypted video conference with a custom key](https://www.infomaniak.com/en/support/faq/2464).

### Technical Specifications
*   **Format:*...

**Key points found:** need kDrive, must be moderator, click action menu (three dots), Start recording, saved to kDrive root, .mp4 format, max 3 hours

#### Q6: How do I set a password for my kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To set a password for your kMeet meeting, follow these steps:

### How to set a password
1. Start **kMeet** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or use the desktop/mobile application.
2. Click on **Start a new meeting**.
3. Enter a **name** for your meeting room.
4. Click on **Security options**.
5. Enable the toggle switch to **Protect access**.
6. Create your **password**.
7. Click **Continue** to start the meeting.
8. Enter the name you wish to use as a participant, then s...

**Key points found:** click security options, enable Protect access toggle, create password, share link AND password, end-to-end encryption option available

#### Q7: How can I livestream a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To livestream a kMeet meeting, you can use the built-in **Live Streaming mode**, which broadcasts your conference via Infomaniak Video Streaming to an unlimited audience.

### Prerequisites & User Roles
*   **Moderator Role:** You must be a moderator of the kMeet meeting to create a live broadcast link.
*   **No Subscription Required:** It is **not necessary** to own an Infomaniak Video Streaming offer to use this feature.
*   **Security Limitation:** You cannot record or stream a meeting if you...

**Key points found:** must be moderator, click action menu, Start live broadcast, copy stream URL to share, max 24 hours, stops when meeting ends

### kDrive (7 questions)

#### Q8: How do I install kDrive on Linux?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To install kDrive on Linux, follow these steps and take note of the specific system requirements and limitations.

### Prerequisites & System Requirements
*   **Operating System:** Officially supported on **Ubuntu 22.04 LTS** (and later).
*   **Desktop Environments:** Officially supported on **GNOME** or **KDE**. 
    *   *Note:* It may work on other distributions, but Infomaniak does not provide support for configurations outside of these.
*   **Required Dependencies:**
    *   **FUSE v2:** Ess...

**Key points found:** .AppImage file, install libfuse2, right-click Permissions, Allow executing file as program, Ubuntu 22.04 LTS officially supported, Lite Sync not available on Linux

#### Q9: How can I share a file from kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To share a file or folder from kDrive, you can use several methods via the web interface.

### Prerequisites
*   To share with specific users (internal or external), the recipient must have an **Infomaniak account** (free or paid).
*   Public share links do not require the recipient to have an account unless specific permissions are set.

### Methods of Sharing

#### 1. Via Public Share Link (No account required for viewing)
This creates a URL that anyone can use to access the file.
*   **How to...

**Key points found:** right-click on file/folder, click Share, public share link option, can set expiration, password, add users with viewing/modification/management rights, recipients can create free Infomaniak account

#### Q10: What is a Drop Box in kDrive and how do I create one?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> A **Drop Box** in kDrive is a secure folder that allows you to invite contacts to deposit files or folders directly into your kDrive. The people you share the link with do not need an Infomaniak account to upload content, and everything they submit is automatically classified in the specific location you have chosen.

### Prerequisites & Role Requirements
*   You must have an active **kDrive** subscription.
*   The number of drop boxes you can create may vary depending on your specific kDrive of...

**Key points found:** invite contacts to deposit files, click New then Drop Box, enter name, can set password, expiration, storage limit, email notification option, disable converts to regular folder

#### Q11: How do I resolve sync conflicts in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> When a synchronization conflict occurs in kDrive, your desktop application icon will turn **orange**. This happens when simultaneous modifications are made to the same file (locally and on the web) or when a file is modified while the application is closed.

### How to View and Resolve Conflicts via the App
1. **Open the kDrive menu**: Click the kDrive icon in your computer's notification area (top right on macOS, bottom right on Windows, or double-click in the taskbar on Linux).
2. **Access det...

**Key points found:** conflicts when same file modified locally and online, kDrive Web version is kept, local saved as _conflict, can keep both, delete, or merge, view via kDrive icon > info, kDrive Rescue Folder for protection

#### Q12: How do I manage user rights in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Managing user rights in kDrive involves two distinct levels: rights within the **kDrive application** itself and rights at the **Organization level** (Manager).

### 1. Managing Rights within the kDrive Web App
To modify a user's permissions directly in kDrive:
*   Log in to the [kDrive Web app](https://ksuite.infomaniak.com/kdrive).
*   Select the relevant kDrive from the left sidebar.
*   Click the **action menu (⋮)** next to the kDrive name and select **Manage users**.
*   Choose the desired ...

**Key points found:** Administrator vs User levels, Administrator has full access, User cannot manage product, Manage users in action menu, don't confuse Manager rights with kDrive rights

#### Q13: How can I access kDrive files locally without downloading them?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To access your kDrive files locally without downloading them to your hard drive, you must use the **Lite Sync** feature. This feature virtually stores your files, making them appear "dehydrated" on your computer and only downloading them when they are opened or modified.

### Prerequisites & Technical Specifications
*   **Operating System:** 
    *   Windows version ≥ 10 (21h2).
    *   macOS version ≥ 10.15.
*   **Processor:** 64-bit processor (ARM64 compatible).
*   **File System:** Must be NT...

**Key points found:** install kDrive desktop app, click icon in notification area, Open kDrive Web for server files, or open local folder, Lite Sync for virtual files

#### Q14: How do I sync kDrive with my Synology NAS?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To synchronize your kDrive with a Synology NAS, you must use the **WebDAV** protocol within the Synology **Cloud Sync** application.

### Prerequisites
*   **External Access:** Your Synology NAS must be accessible from the Internet.
*   **kDrive ID:** You must know your kDrive identifier (kDrive ID).
*   **Application Password:** You must create a specific application password from your Infomaniak account for this connection (do not use your main account password).

### How to use Cloud Sync wit...

**Key points found:** use Cloud Sync app, choose WebDAV, use application password, Bidirectional, Download remote, or Download local sync
**Key points missing:** server: https://[kDriveID].connect.kdrive.infomaniak.com

### kChat (6 questions)

#### Q15: How do I create a channel in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create a new channel in kChat, follow these steps and review the associated requirements:

### Prerequisites and User Roles
*   You must have sufficient permissions to administer the chat service within your Organization.
*   You must have an active kSuite offer.

### How to Create a Channel
1.  Access the **kChat web app** ([ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat)) or the **kChat desktop app**.
2.  Click on the **+** (plus) button located in the left sidebar.
3.  Se...

**Key points found:** click button in left sidebar, Create a new channel, set name, URL, private/public, description, General channel exists by default, can convert, leave, archive channels

#### Q16: What slash commands are available in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> In kChat, slash commands are messages starting with a `/` (forward slash) that are interpreted as specific actions.

### How to use
*   Click in the message composition field of any channel.
*   Type `/` followed by the command name.
*   If you type only the `/` sign, a modal will appear listing the commands available to you.
*   Press Enter or confirm to execute the command.

### Available Slash Commands
While the documentation mentions that a full list appears in the help modal when typing `/`...

**Key points found:** type / followed by command, just / shows available commands, can create custom slash commands, go to Integrations > Slash command, custom commands can call APIs, external users cannot access Integrations

#### Q17: How can I connect external applications to kChat?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> To connect external applications to kChat, you can use **Webhooks** (Incoming and Outgoing) and **Slash Commands**. These tools allow kChat to communicate with third-party or self-hosted applications.

### Prerequisites
*   **User Role:** You must not be an "external user." External users cannot see the *Integrations* menu.
*   **Access:** You must use the kChat Web app (ksuite.infomaniak.com/kchat) or the kChat desktop application (macOS, Windows, Linux).

### Platform Limitations & Technical S...

**Key points found:** use webhooks, Integrations menu, Incoming webhooks receive from external apps, Outgoing webhooks send to external apps, external users cannot access Integrations
**Key points missing:** POST request with JSON text field

#### Q18: How do I translate a message in kChat?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To translate a message in kChat, follow these steps:

### How to use
The automatic translation service is integrated into the kChat app to help you read messages received in a foreign language.
1. Access **kChat** via the web app ([ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat)), the mobile app (iOS/Android), or the desktop app (macOS/Windows/Linux).
2. Navigate to the conversation containing the message you wish to translate.
3. Click on the **action menu (•••)** located at t...

**Key points found:** click action menu (three dots) on message, click Translate, translation appears below, only visible to you
**Key points missing:** translates to your language

#### Q19: How can I invite external users to kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To invite external users to kChat, you have two main options depending on whether you want them to be counted as a kSuite user or remain a "restricted" external guest.

### 1. Invite as a Restricted External User (Guest)
This method allows you to grant access to specific channels without the user being part of your Organization or counting toward your kSuite user quota.

*   **Prerequisites:** You must be the administrator of the Organization with full rights granted for kChat.
*   **User Role/P...

**Key points found:** must be Organization administrator, click Invite members, enter email and specify channels, users receive email invitation, external users not counted as users, guests have limited permissions

#### Q20: What is Euria and how do I use it in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> **Euria** is the artificial intelligence integrated into Infomaniak's kSuite. On **kChat**, it functions as a conversational agent that can perform calculations, translate text, provide information on various subjects, and summarize discussions.

### Prerequisites & User Roles
*   **Activation:** An **Administrator or Legal Representative** must activate Euria for the Organization through the unified settings or the kDrive assistant.
*   **Content Search:** Content search features on documents m...

**Key points found:** Euria is AI assistant in kSuite, calculations, translations, information, search for bot in channel search, create private discussion with bot, do not create group conversation, new users get welcome message

---

## Recommendations

- **Good coverage achieved.** Focus on:
  - Response latency optimization
  - Edge case handling