# RAG Quality Evaluation Report

**Generated:** 2026-01-16 21:42:41
**Questions Tested:** 20

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Score | 60/60 (100.0%) |
| Average Score | 3.00/3.00 |
| Average Coverage | 98.0% |
| Average Response Time | 23.8s |

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
> Here is a complete guide to creating a **kMeet meeting**, including prerequisites, platform limitations, and step-by-step instructions:

---

### **How to Create a kMeet Meeting**
#### **Prerequisites**
- No Infomaniak account is required to **create or join** a meeting.
- To **record the meeting** or use advanced features (e.g., participant control, password protection), you must:
  - Be the **first to join the meeting** (automatically granted moderator status).
  - Or be **designated as a mode...

**Key points found:** kmeet.infomaniak.com, enter meeting room name, allow webcam/microphone access, click Join the meeting, share room link

#### Q2: How can I share my screen during a kMeet call?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> Here’s how you can share your screen during a **kMeet** call, along with important details and limitations:

---

### **How to Share Your Screen on kMeet**
#### **Prerequisites**
- You must be in an active **kMeet meeting** (created or joined).
- Screen sharing is available on:
  - **Desktop apps** (macOS, Windows, Linux).
  - **Web app** (via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) in browsers like Chrome or Firefox).
  - **Mobile apps** (Android only).
    **⚠️ Not available on iO...

**Key points found:** click screen icon with arrow, choose entire screen or specific window, not available on iOS, stop by clicking toolbar icon
**Key points missing:** validate authorization

#### Q3: What should I do if my audio is not working in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> If your audio is not working in **kMeet**, follow these troubleshooting steps:

---

### **Prerequisites**
- You must have a **microphone** connected to your device (built-in or external).
- You must have granted **microphone permissions** to kMeet in your browser or desktop app.
- You must be using a **supported browser** (Chrome, Firefox, Safari, Edge) or the **kMeet desktop/mobile app**.

---

### **Troubleshooting Steps**

#### **1. Check Microphone Permissions**
- **For browsers (Web versio...

**Key points found:** check Settings for microphone permission, browser lock icon, mobile Privacy settings, Windows Audio Troubleshooter, try different device, Firefox WebRTC disable option

#### Q4: How do I create side rooms (breakout rooms) in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to create **side rooms (breakout rooms)** in kMeet:

---

### **Prerequisites**
- You **must be a moderator** of the kMeet meeting. Only moderators can create and manage side rooms.
- Participants can join side rooms but cannot create them.
- Side rooms are available on **all platforms** (Web, macOS, Windows, Linux, iOS, and Android).

---

### **How to Create Side Rooms (Breakout Rooms)**
1. **Start a kMeet meeting** as a moderator:
   - Go to [kmeet.infomaniak.com](https://kmeet.inf...

**Key points found:** must be moderator, click multi-user icon, add side room button, participants can join/leave, moderator can force participants to join

#### Q5: How can I record a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how you can record a **kMeet meeting**, along with all relevant details from the documentation:

---

### **How to Record a kMeet Meeting**
#### **Prerequisites**
- You **must have a kDrive** (standalone or as part of a kSuite/my kSuite).
- You **must be the moderator** of the video conference.
- The meeting **must not be encrypted with a custom key** (recording is not supported in this case).

---

#### **Platform Limitations**
- Recording is **available on all platforms** (Web, macOS, W...

**Key points found:** need kDrive, must be moderator, click action menu (three dots), Start recording, saved to kDrive root, .mp4 format, max 3 hours

#### Q6: How do I set a password for my kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to set a password for your **kMeet meeting**:

---

### **Prerequisites**
- You must be the **meeting organizer** or **moderator** (the first person to start the meeting).
- The password must be shared with participants so they can join.
- Password protection can be enabled **during meeting creation** or **before participants join**.

---

### **Steps to Set a Password for a kMeet Meeting**
1. **Start kMeet**:
   - Go to **[kmeet.infomaniak.com](https://kmeet.infomaniak.com/)** or ope...

**Key points found:** click security options, enable Protect access toggle, create password, share link AND password, end-to-end encryption option available

#### Q7: How can I livestream a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to **livestream a kMeet meeting** using the **Live Streaming mode**:

---

### **Prerequisites**
- You **must be a moderator** of the kMeet meeting to start a livestream.
- You **do not need** an Infomaniak Video Streaming subscription to create a livestream link.
- The livestream is accessible via a **unique URL** and can be viewed by an **unlimited number of participants**.
- The livestream **stops automatically** when the kMeet meeting ends.
- The maximum duration of the livestream...

**Key points found:** must be moderator, click action menu, Start live broadcast, copy stream URL to share, max 24 hours, stops when meeting ends

### kDrive (7 questions)

#### Q8: How do I install kDrive on Linux?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to install **kDrive on Linux** based on the official Infomaniak documentation:

---

### **Prerequisites**
- A **Linux** system with:
  - **Ubuntu 22.04 LTS** (or later) **officially supported**.
  - Desktop environments: **GNOME** or **KDE** (officially supported).
  - *Note: kDrive may work on other distributions or desktop environments, but Infomaniak provides no support for unsupported configurations.*
- Download the **kDrive desktop app** for Linux (file type: `.AppImage`):
  - D...

**Key points found:** .AppImage file, install libfuse2, right-click Permissions, Allow executing file as program, Ubuntu 22.04 LTS officially supported, Lite Sync not available on Linux

#### Q9: How can I share a file from kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how you can share a file from **kDrive**, along with all relevant details:

---

### **How to Share a File from kDrive**
You can share files or folders from kDrive in multiple ways, depending on your needs (e.g., public link, direct share with kDrive users, or via email).

---

#### **Prerequisites**
- You must have a **kDrive account** (free or paid).
- The file/folder you want to share must be uploaded to your kDrive.
- For **external shares** (users outside your kDrive), the recipient ...

**Key points found:** right-click on file/folder, click Share, public share link option, can set expiration, password, add users with viewing/modification/management rights, recipients can create free Infomaniak account

#### Q10: What is a Drop Box in kDrive and how do I create one?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here is a detailed explanation of what a **Drop Box** is in kDrive and how to create one:

---

### **What is a Drop Box in kDrive?**
A **Drop Box** in kDrive is a feature that allows you to:
- Create a dedicated space where **external contacts** (or internal users) can **upload files or folders directly to your kDrive**.
- Collect data in a specific folder on your kDrive without granting access to the rest of your files.
- Customize the Drop Box with options like:
  - **Email notifications** wh...

**Key points found:** invite contacts to deposit files, click New then Drop Box, enter name, can set password, expiration, storage limit, email notification option, disable converts to regular folder

#### Q11: How do I resolve sync conflicts in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to resolve sync conflicts in **kDrive**, based on the official documentation:

---

### **Prerequisites**
- You must have the **kDrive desktop app** installed (macOS, Windows, or Linux).
- Conflicts typically occur when the **same file is modified simultaneously** on multiple devices or on **kDrive Web** while the app is offline.
- Conflicts are **not automatically resolved** for all cases; manual intervention may be required.

---

### **How Sync Conflicts Occur**
Conflicts arise in ...

**Key points found:** conflicts when same file modified locally and online, kDrive Web version is kept, local saved as _conflict, can keep both, delete, or merge, view via kDrive icon > info, kDrive Rescue Folder for protection

#### Q12: How do I manage user rights in kDrive?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s a comprehensive guide on how to manage user rights in **kDrive**, based on the official Infomaniak documentation:

---

### **How to Manage User Rights in kDrive**
#### **Prerequisites**
- You must have **Administrator** or **Legal Representative** access to the **Organization** or **kDrive** in question.
- You must be using the **kDrive Web app** (accessible via [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
- For advanced actions (e.g., replacing a user), you mus...

**Key points found:** Administrator vs User levels, Administrator has full access, User cannot manage product, Manage users in action menu, don't confuse Manager rights with kDrive rights

#### Q13: How can I access kDrive files locally without downloading them?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To access your **kDrive files locally without downloading them entirely**, you can use the **Lite Sync** feature available in the kDrive desktop app (for **Windows** and **macOS**). This allows you to view and access files virtually without occupying full storage space on your device. Here’s how it works:

---

### **Prerequisites**
- Install the **[kDrive desktop app](https://www.infomaniak.com/en/support/faq/2374)** on your **Windows** or **macOS** device.
- Ensure you are logged in to your In...

**Key points found:** install kDrive desktop app, click icon in notification area, Open kDrive Web for server files, or open local folder, Lite Sync for virtual files

#### Q14: How do I sync kDrive with my Synology NAS?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> Here’s how to sync **kDrive with your Synology NAS** using the **WebDAV** protocol via the **Cloud Sync** app:

---

### **Prerequisites**
- A **Synology NAS** accessible from the Internet.
- Your **[kDrive identifier (kDrive ID)](https://www.infomaniak.com/en/support/faq/2409)** (e.g., `12345`).
- An **Infomaniak account email address** and an **[application password](https://www.infomaniak.com/en/support/faq/2356)** (do not use your main account password).

---

### **Platform Limitations**
- ...

**Key points found:** use Cloud Sync app, choose WebDAV, use application password, Bidirectional, Download remote, or Download local sync
**Key points missing:** server: https://[kDriveID].connect.kdrive.infomaniak.com

### kChat (6 questions)

#### Q15: How do I create a channel in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to create a channel in **kChat**, along with important details:

---

### **How to Create a Channel in kChat**
#### **Prerequisites**
- You must be a member of a **kChat Organization** (part of kSuite).
- No specific role is required to create a **public channel**, but you must be invited to create or join a **private channel**.

---

#### **Steps to Create a Channel**
1. **Access kChat**:
   - Open the **kChat web app** ([ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kch...

**Key points found:** click button in left sidebar, Create a new channel, set name, URL, private/public, description, General channel exists by default, can convert, leave, archive channels

#### Q16: What slash commands are available in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here are the **slash commands** available in **kChat**, along with their functionalities, prerequisites, and limitations:

---

### **Default Slash Commands in kChat**
To use a slash command:
1. Open a channel or direct message in kChat.
2. Type `/` in the message composition field.
3. Select a command from the list or type it manually (e.g., `/away`).
4. Press **Enter** to execute the command.

---

#### **List of Default Slash Commands**
| Command               | Description                   ...

**Key points found:** type / followed by command, just / shows available commands, can create custom slash commands, go to Integrations > Slash command, custom commands can call APIs, external users cannot access Integrations

#### Q17: How can I connect external applications to kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To connect external applications to **kChat**, you can use **webhooks** (incoming and outgoing) to integrate third-party applications or custom solutions. Here’s how to do it:

---

### **Prerequisites**
- You **must not be an external user** (external users cannot access the *Integrations* menu).
- You need access to the **kChat Web app** ([ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat)) or the **kChat desktop app** (macOS, Windows, Linux).
- For advanced integrations (e.g., ...

**Key points found:** use webhooks, Integrations menu, Incoming webhooks receive from external apps, Outgoing webhooks send to external apps, POST request with JSON text field, external users cannot access Integrations

#### Q18: How do I translate a message in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to translate a message in **kChat**:

---

### **How to Translate a Message in kChat**
You can translate messages in kChat directly from the web, desktop (macOS/Windows/Linux), or mobile (iOS/Android) apps.

---

#### **Prerequisites**
- You must be a member of the kChat organization where the message was sent.
- The translation feature is available for messages written in a foreign language.

---

#### **Steps to Translate a Message**
1. **Open kChat**:
   - Access the [kChat web app...

**Key points found:** click action menu (three dots) on message, click Translate, translation appears below, only visible to you, translates to your language

#### Q19: How can I invite external users to kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> Here’s how to invite external users to **kChat**, along with important details about permissions, prerequisites, and limitations:

---

### **How to Invite External Users to kChat**
#### **Prerequisites**
- You must have **administrator or full rights** for kChat in your Organization.
- The external user must **create an Infomaniak account** if they don’t already have one.
- External users **do not count** toward your kSuite user quota.

---

#### **Steps to Invite an External User**
1. **Access...

**Key points found:** must be Organization administrator, click Invite members, enter email and specify channels, users receive email invitation, external users not counted as users, guests have limited permissions

#### Q20: What is Euria and how do I use it in kChat?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> ### **What is Euria?**
Euria is an **artificial intelligence (AI)** integrated into **kSuite**, particularly within **kChat**. It acts as a conversational agent to assist you with various tasks, such as:
- Answering questions on a wide range of topics.
- Performing calculations and translations.
- Summarizing discussions or threads in kChat.
- Providing information or explanations based on the context of your conversations.
- Sending welcome messages to new users automatically.

Euria is also av...

**Key points found:** Euria is AI assistant in kSuite, calculations, translations, information, search for bot in channel search, create private discussion with bot, do not create group conversation, new users get welcome message

---

## Recommendations

- **Good coverage achieved.** Focus on:
  - Response latency optimization
  - Edge case handling