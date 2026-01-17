# RAG Quality Evaluation Report

**Generated:** 2026-01-16 21:27:56
**Questions Tested:** 20

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Score | 44/48 (91.7%) |
| Average Score | 2.75/3.00 |
| Average Coverage | 87.7% |
| Average Response Time | 15.9s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 14 | 87.5% |
| Partial (2) | 1 | 6.2% |
| Minimal (1) | 0 | 0.0% |
| Wrong (0) | 1 | 6.2% |

---

## Detailed Results

### kMeet (7 questions)

#### Q1: How do I create a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create a kMeet meeting, you have two main options:

## Option 1: Quick Meeting (No Registration Required)

- Go to [kmeet.infomaniak.com](https://kmeet.infomaniak.com/) in your browser
- Click **"Start a new meeting"**
- Enter a **name** for your meeting room
- Allow access to your webcam and microphone when prompted
- Enter your **name or pseudonym** that other participants will see
- Optionally enable participant control, password, or custom encryption key
- Click **"Join the meeting"**
- *...

**Key points found:** kmeet.infomaniak.com, enter meeting room name, allow webcam/microphone access, click Join the meeting, share room link

#### Q2: How can I share my screen during a kMeet call?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To share your screen during a kMeet call, follow these steps:

### Prerequisites
- You must use one of the following:
  - **kMeet desktop app** (macOS, Windows, or Linux)
  - **kMeet mobile app** on **Android** devices
  - **Web version** at [kmeet.infomaniak.com](https://kmeet.infomaniak.com)
- **Screen sharing is NOT available on iOS** (iPhone/iPad) devices.
- If it’s your first time sharing your screen, your operating system or browser may request permissions, and you might need to **restart ...

**Key points found:** click screen icon with arrow, choose entire screen or specific window, not available on iOS, stop by clicking toolbar icon
**Key points missing:** validate authorization

#### Q3: What should I do if my audio is not working in kMeet?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> If your audio is not working in kMeet, follow these troubleshooting steps:

### 1. (Re)authorize microphone access on your computer
- Go to **kMeet Settings** (click the icon at the top right of the interface)
- Reactivate permission requests for multimedia functions:
  - Grant access to a microphone (choose your preferred device)
  - Grant access to the camera if needed
- Check your browser's address bar for a **lock icon** that might be blocking multimedia access, and click on it to allow perm...

**Key points found:** check Settings for microphone permission, browser lock icon, mobile Privacy settings, Windows Audio Troubleshooter, try different device
**Key points missing:** Firefox WebRTC disable option

#### Q4: How do I create side rooms (breakout rooms) in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create side rooms (breakout rooms) in kMeet, follow these steps:

## Prerequisites
- **You must be a moderator** of the kMeet meeting to create and manage breakout rooms
- Side rooms can only be created **during an active meeting** when participants are already present

## How to Create Side Rooms

1. **Start kMeet as a moderator** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the applications for computer or mobile devices
2. **Wait for participants to join** the me...

**Key points found:** must be moderator, click multi-user icon, add side room button, participants can join/leave, moderator can force participants to join

#### Q5: How can I record a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To record a kMeet meeting, you need to meet the following **prerequisites**:

- Have a **kDrive** (standalone or as part of a kSuite, my kSuite, etc.)
- Be the **moderator** of the video conference
- **Not** be using an [encrypted video conference with a custom key](https://www.infomaniak.com/en/support/faq/2464)

### How to record a kMeet meeting:

1. Start **kMeet** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the [apps](https://infomaniak.com/gtl/apps.kmeet) for com...

**Key points found:** need kDrive, must be moderator, click action menu (three dots), Start recording, saved to kDrive root, .mp4 format, max 3 hours

#### Q6: How do I set a password for my kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To set a password for your kMeet meeting, follow these steps:

- Start kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the applications for computers or mobile devices.
- Start a new meeting.
- Enter a **name** for your meeting room.
- Click on the **security options**.
- Enable the toggle switch to **Protect access**.
- Create the password.
- Click **Continue** to **start** the meeting.
- Share the **meeting link or code** and the **password** with your participant...

**Key points found:** click security options, enable Protect access toggle, create password, share link AND password, end-to-end encryption option available

#### Q7: How can I livestream a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To livestream a kMeet meeting, you need to use Infomaniak’s **Video Streaming** feature. Here’s how:

### Prerequisites
- You **must be a moderator** of the kMeet meeting.
- You **do not need** to own an Infomaniak Video Streaming subscription to create a live broadcast link.

### Steps to Start Livestreaming
1. Start your meeting via [ksuite.infomaniak.com/kmeet](https://ksuite.infomaniak.com/kmeet) or using the kMeet desktop/mobile app.
2. Once in the meeting, click the **action menu (○○○)** i...

**Key points found:** must be moderator, click action menu, Start live broadcast, copy stream URL to share, max 24 hours, stops when meeting ends

### kDrive (5 questions)

#### Q8: How do I install kDrive on Linux?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To install kDrive on Linux, follow these steps and prerequisites:

### Prerequisites
- **Supported Systems**: kDrive is officially supported only on:
  - Ubuntu 22.04 LTS (and later)
  - Desktop environments: GNOME or KDE
- **Required Packages**:
  - Download the kDrive desktop app for Linux (file type: `.AppImage`)
  - **libfuse2**: Required to run AppImage files (especially on Ubuntu 23.04 and later where FUSE v3 is default, but AppImage needs FUSE v2)
    ```bash
    sudo apt install libfuse2...

**Key points found:** .AppImage file, install libfuse2, right-click Permissions, Allow executing file as program, Ubuntu 22.04 LTS officially supported, Lite Sync not available on Linux

#### Q9: How can I share a file from kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To share a file from kDrive, you have several options depending on whether you want to share it with specific people or create a public link. Here's how to do it:

### **Option 1: Share via Public Link (Anyone with the link can access)**
- **Prerequisites**: None – works even if the recipient doesn’t have an Infomaniak account.
- **Steps**:
  1. Go to the [kDrive web app](https://ksuite.infomaniak.com/kdrive).
  2. Right-click on the file or folder you want to share.
  3. Click **Share**.
  4. I...

**Key points found:** right-click on file/folder, click Share, public share link option, can set expiration, password, add users with viewing/modification/management rights, recipients can create free Infomaniak account

#### Q12: How do I manage user rights in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To manage user rights in kDrive, you need to understand that there are **two distinct levels** of permissions:

1. **Organization-level rights** (product management access in the Infomaniak Manager)
2. **kDrive-specific rights** (permissions within the kDrive application itself)

## Organization-Level Rights (Product Management)

These control access to manage the kDrive service in the Infomaniak Manager:

- **Technical rights**: Access to dashboard, sharing links, user management
- **Statistics...

**Key points found:** Administrator vs User levels, Administrator has full access, User cannot manage product, Manage users in action menu, don't confuse Manager rights with kDrive rights

#### Q13: How can I access kDrive files locally without downloading them?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> You can access kDrive files locally without downloading them by using the **Lite Sync** feature of the kDrive desktop app. This feature virtually stores your files on your computer and only downloads them when needed, saving disk space.

### Prerequisites:
- Install the [kDrive desktop app](https://www.infomaniak.com/en/support/faq/2374) on your device (Windows, macOS, or Linux).

### Steps to access files locally without full download:
1. **Install and launch** the kDrive desktop app.
2. During...

**Key points found:** install kDrive desktop app, click icon in notification area, Open kDrive Web for server files, or open local folder, Lite Sync for virtual files

#### Q14: How do I sync kDrive with my Synology NAS?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To sync kDrive with your Synology NAS, you need to use the **WebDAV protocol** through the **Cloud Sync** application on your Synology NAS. Here's how to do it:

### Prerequisites
- You must have a Synology NAS accessible from the Internet.
- You need to know your **kDrive ID** ([how to find it](https://www.infomaniak.com/en/support/faq/2409)).

### Steps to synchronize
1. Log in to your **Synology DiskStation Manager (DSM)**.
2. If not already installed, download and install the **Cloud Sync** ...

**Key points found:** use Cloud Sync app, choose WebDAV, use application password, Bidirectional, Download remote, or Download local sync
**Key points missing:** server: https://[kDriveID].connect.kdrive.infomaniak.com

### kChat (4 questions)

#### Q17: How can I connect external applications to kChat?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> You can connect external applications to **kChat** using **webhooks**. Here's how:

### Prerequisites
- You must **not be an external user**, as external users cannot see the *Integrations* menu.

### What are webhooks?
- **Incoming webhook**: Allows external apps to send data to kChat, which can trigger actions like posting messages in a channel.
- **Outgoing webhook**: Allows kChat to send data to other apps when specific events occur in kChat.

### How to set up an incoming webhook
1. Go to t...

**Key points found:** use webhooks, Integrations menu, Incoming webhooks receive from external apps, Outgoing webhooks send to external apps, external users cannot access Integrations
**Key points missing:** POST request with JSON text field

#### Q18: How do I translate a message in kChat?

**Rating:** [~] Partial (60.0% coverage)

**Response excerpt:**
> To translate a message in kChat, follow these steps:

- Access kChat via:
  - The [web app](https://ksuite.infomaniak.com/kchat)
  - The mobile app (iOS/Android)
  - The desktop app (macOS/Windows/Linux)

- View the message you want to translate
- Click on the **action menu •••** located at the top right of the message
- Click on **Translate**
- The translated message will appear below your conversation and is **only visible to you**

Source: https://www.infomaniak.com/en/support/faq/1467/transl...

**Key points found:** click action menu (three dots) on message, click Translate, only visible to you
**Key points missing:** translation appears below, translates to your language

#### Q19: How can I invite external users to kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To invite external users to kChat, you can follow these steps:

### Prerequisites
- You must be the administrator of the Organization with full rights granted for kChat.
- External users will not be counted as kSuite users and will have limited permissions (referred to as "guests").

### Steps to Invite External Users:
1. **Access kChat**:
   - Go to the [kChat Web app](https://ksuite.infomaniak.com/kchat) or open the kChat desktop app (available on macOS, Windows, and Linux).

2. **Invite Membe...

**Key points found:** must be Organization administrator, click Invite members, enter email and specify channels, users receive email invitation, external users not counted as users, guests have limited permissions

#### Q20: What is Euria and how do I use it in kChat?

**Rating:** [x] Wrong (16.7% coverage)

**Response excerpt:**
> Euria is Infomaniak's artificial intelligence assistant integrated into kChat. It can answer questions, generate content, and assist with various tasks directly within the chat interface.

To use Euria in kChat:

- Type `/` followed by the command name to access Euria's features
- You can ask Euria questions or request content generation directly in chat

**Important details about Euria:**

- Euria is available as a built-in feature in kChat
- It can be accessed through slash commands in any cha...

**Key points found:** Euria is AI assistant in kSuite
**Key points missing:** calculations, translations, information, search for bot in channel search, create private discussion with bot, do not create group conversation, new users get welcome message

---

## Recommendations

- **Good coverage achieved.** Focus on:
  - Response latency optimization
  - Edge case handling
- **1 wrong responses detected.** Review these questions for retrieval issues.