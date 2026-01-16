# RAG Quality Evaluation Report

**Generated:** 2026-01-16 19:30:55
**Questions Tested:** 20

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Score | 47/60 (78.3%) |
| Average Score | 2.35/3.00 |
| Average Coverage | 73.0% |
| Average Response Time | 13.1s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 9 | 45.0% |
| Partial (2) | 9 | 45.0% |
| Minimal (1) | 2 | 10.0% |
| Wrong (0) | 0 | 0.0% |

---

## Detailed Results

### kMeet (7 questions)

#### Q1: How do I create a kMeet meeting?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> To create a kMeet meeting, follow these steps:

1. **Start kMeet**:
   - Go to [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or use the kMeet application on your computer or mobile device.

2. **Create a new meeting**:
   - Click on the option to start a new meeting.

3. **Configure the meeting**:
   - Enter a **name** for your meeting room.
   - Allow access to your webcam and microphone.
   - Enter your **pseudonym** or **first and last name**.

4. **Set security options (optional)**:
 ...

**Key points found:** kmeet.infomaniak.com, enter meeting room name, allow webcam/microphone access, click Join the meeting, share room link

#### Q2: How can I share my screen during a kMeet call?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To share your screen during a kMeet call, follow these steps:

1. Start kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the applications for computers or mobile devices.
2. Create or join a meeting room.
3. Click on the screen icon with an arrow to **Share your screen**.
4. Read the warning that may be displayed by your device and validate the authorization to access the screen content.
5. Choose whether to share your entire screen or a specific window.
6. Click the...

**Key points found:** click screen icon with arrow, choose entire screen or specific window, validate authorization, stop by clicking toolbar icon
**Key points missing:** not available on iOS

#### Q3: What should I do if my audio is not working in kMeet?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> If your audio is not working in kMeet, follow these steps to troubleshoot the issue:

### General Tips
1. **Reauthorize Multimedia Access**:
   - Go to **Settings** in kMeet (click the gear icon at the top right).
   - Ensure access to the microphone is enabled and select the correct device.
   - Check for a lock icon in your browser's address bar that might be blocking access and click it to adjust permissions.
   - Source: [Fix an audio issue on kMeet](https://www.infomaniak.com/en/support/faq...

**Key points found:** check Settings for microphone permission, browser lock icon, mobile Privacy settings, Windows Audio Troubleshooter, try different device, Firefox WebRTC disable option

#### Q4: How do I create side rooms (breakout rooms) in kMeet?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To create side rooms (breakout rooms) in kMeet, follow these steps:

1. **Start kMeet as a moderator**: Open kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or use the kMeet application on your computer or mobile device.
2. **Join the meeting**: Ensure all participants are in the meeting.
3. **Access the side rooms feature**: Click on the multi-user icon in the kMeet toolbar.
4. **Create a side room**: Click the button to add a side room.
5. **Manage participants**: Participants c...

**Key points found:** click multi-user icon, add side room button, participants can join/leave, moderator can force participants to join
**Key points missing:** must be moderator

#### Q5: How can I record a kMeet meeting?

**Rating:** [-] Minimal (42.9% coverage)

**Response excerpt:**
> To record a kMeet meeting, follow these steps:

1. Start **kMeet** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the apps for computers and mobile devices.
2. Once in the meeting, click on the action menu **○○○** in the kMeet toolbar.
3. Click on the icon ◉ **Start recording**.
4. Confirm the operation and, if necessary, log in to your Infomaniak account. Then, select a kDrive to record the video conference on and click the button to start.
5. To stop recording, click o...

**Key points found:** click action menu (three dots), Start recording, saved to kDrive root
**Key points missing:** need kDrive, must be moderator, .mp4 format, max 3 hours

#### Q6: How do I set a password for my kMeet meeting?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To set a password for your kMeet meeting, follow these steps:

1. Start kMeet via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or from one of the applications for computers or mobile devices.
2. Start a new meeting.
3. Enter a **name** for your meeting room.
4. Click on the **security options**.
5. Enable the toggle switch to **Protect access**.
6. Create the password.
7. **Continue** to **start** the meeting.
8. Specify the name you want to use as a participant in the meeting.
9. Share ...

**Key points found:** click security options, enable Protect access toggle, create password, share link AND password
**Key points missing:** end-to-end encryption option available

#### Q7: How can I livestream a kMeet meeting?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To livestream a kMeet meeting, follow these steps:

1. **Start the kMeet Meeting**:
   - Open kMeet via [ksuite.infomaniak.com/kmeet](https://ksuite.infomaniak.com/kmeet) or use the kMeet app on your computer or mobile device.

2. **Initiate the Live Broadcast**:
   - Once in the meeting, click on the action menu (**○○○**) in the kMeet toolbar.
   - Select **Start live broadcast**.

3. **Start the Stream**:
   - Click the **Start** button to begin the live broadcast.

4. **Share the Stream Link*...

**Key points found:** click action menu, Start live broadcast, copy stream URL to share, max 24 hours
**Key points missing:** must be moderator, stops when meeting ends

### kDrive (7 questions)

#### Q8: How do I install kDrive on Linux?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To install kDrive on Linux, follow these steps:

### Prerequisites
- Ensure you are using **Ubuntu 22.04 LTS** or later with **GNOME** or **KDE** desktop environments.
- Download the kDrive AppImage file for Linux.
- Install the required dependencies:
  - **Fuse2**: Required to run AppImage. Install it using:
    ```bash
    sudo apt install libfuse2
    ```
  - **D-Bus**
  - **Gnome-keyring** or **kwallet** (usually pre-installed except on some lightweight distributions).

### Installation Step...

**Key points found:** install libfuse2, right-click Permissions, Allow executing file as program, Ubuntu 22.04 LTS officially supported
**Key points missing:** .AppImage file, Lite Sync not available on Linux

#### Q9: How can I share a file from kDrive?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To share a file from kDrive, follow these steps:

1. Access the kDrive web app by clicking [here](https://ksuite.infomaniak.com/kdrive).
2. Right-click on the file or folder you want to share.
3. Click on **Share** at the top of the dropdown menu.

From there, you have two options:

### Option 1: Public Share Link
- Activate the **public share link**.
- Customize the sharing options:
  - Allow modifications (if the file is in a collaborative format).
  - Set an expiration date.
  - Add a passwor...

**Key points found:** right-click on file/folder, click Share, public share link option, add users with viewing/modification/management rights
**Key points missing:** can set expiration, password, recipients can create free Infomaniak account

#### Q10: What is a Drop Box in kDrive and how do I create one?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> A **Drop Box** in kDrive is a feature that allows you to create a dedicated folder where external contacts can upload files or folders directly into your kDrive. This is useful for collecting content from others without giving them full access to your kDrive.

### How to Create a Drop Box in kDrive:

1. **Access kDrive**:
   - Go to the [kDrive Web app](https://ksuite.infomaniak.com/kdrive).

2. **Navigate to the Desired Folder**:
   - Choose the folder where you want the Drop Box to be created ...

**Key points found:** invite contacts to deposit files, click New then Drop Box, enter name, email notification option
**Key points missing:** can set password, expiration, storage limit, disable converts to regular folder

#### Q11: How do I resolve sync conflicts in kDrive?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To resolve sync conflicts in kDrive, follow these steps:

### Displaying Conflicts
1. Left-click on the kDrive desktop app icon in your computer's notification area.
2. Click on the information button at the top.
3. Click on the listed event to view its details.
4. Conflicts and errors are displayed in two distinct tabs, allowing you to identify unsynchronized data.

### Resolving Conflicts
1. Choose how to resolve the conflict:
   - Send the local version to the server (synchronize).
   - Move ...

**Key points found:** conflicts when same file modified locally and online, kDrive Web version is kept, view via kDrive icon > info, kDrive Rescue Folder for protection
**Key points missing:** local saved as _conflict, can keep both, delete, or merge

#### Q12: How do I manage user rights in kDrive?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To manage user rights in kDrive, follow these steps:

1. **Access kDrive**:
   - Go to the [Infomaniak kDrive Web app](https://ksuite.infomaniak.com/kdrive).
   - Select the relevant kDrive from the dropdown menu in the left sidebar.

2. **Manage User Rights**:
   - Click on the **action menu ⋮** next to the relevant item.
   - Select **Manage users**.
   - Choose the desired access level for the user:
     - **Administrator**: Grants full rights, including sharing, statistics, and managing fold...

**Key points found:** Administrator vs User levels, Administrator has full access, User cannot manage product, Manage users in action menu
**Key points missing:** don't confuse Manager rights with kDrive rights

#### Q13: How can I access kDrive files locally without downloading them?

**Rating:** [+] Complete (100.0% coverage)

**Response excerpt:**
> You can access your kDrive files locally without downloading them by using the **Lite Sync** feature in the kDrive desktop app. This feature allows you to view and manage files directly from your computer without taking up storage space, as the files remain stored in the cloud and are only downloaded when needed.

### Steps to Enable Lite Sync:
1. Install the [kDrive desktop app](https://www.infomaniak.com/en/support/faq/2374) on your device.
2. Open the kDrive app and click on the app icon in t...

**Key points found:** install kDrive desktop app, click icon in notification area, Open kDrive Web for server files, or open local folder, Lite Sync for virtual files

#### Q14: How do I sync kDrive with my Synology NAS?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To sync kDrive with your Synology NAS, follow these steps:

1. **Prerequisites:**
   - Ensure your Synology NAS is accessible from the Internet.
   - Know your kDrive identifier (kDrive ID). You can find it [here](https://www.infomaniak.com/en/support/faq/2409).

2. **Steps to Sync:**
   - Log in to the Synology DiskStation Manager (DSM).
   - If necessary, download and install the **Cloud Sync** app from the **Package Center**.
   - Open **Cloud Sync**.
   - Click on the **+** at the bottom lef...

**Key points found:** use Cloud Sync app, choose WebDAV, use application password, Bidirectional, Download remote, or Download local sync
**Key points missing:** server: https://[kDriveID].connect.kdrive.infomaniak.com

### kChat (6 questions)

#### Q15: How do I create a channel in kChat?

**Rating:** [-] Minimal (40.0% coverage)

**Response excerpt:**
> To create a channel in kChat, follow these steps:

1. Open the **kChat** web app: [ksuite.infomaniak.com/kchat](https://ksuite.infomaniak.com/kchat).
2. Click on the button located in the left sidebar.
3. Select **Create a new channel**.
4. Configure the channel by setting:
   - **Name**: The name of the channel (modifiable later).
   - **URL**: The URL of the channel (modifiable later).
   - **Status**: Choose whether the channel is **PRIVATE** or **PUBLIC** (modifiable later).
   - **Descripti...

**Key points found:** click button in left sidebar, Create a new channel
**Key points missing:** set name, URL, private/public, description, General channel exists by default, can convert, leave, archive channels

#### Q16: What slash commands are available in kChat?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> Here are the available slash commands in kChat:

- **Execute a slash command**:
  - Click in the composition field within a channel.
  - Enter a `/` (slash or forward slash) followed by the command.
  - Confirm to send the command.
  - Typing only `/` will display a modal with available commands, such as going offline.

- **Create a custom slash command**:
  - Access the Web kChat app or the desktop kChat app.
  - Click on the **New** icon next to your kChat organization name.
  - Click on **Int...

**Key points found:** type / followed by command, just / shows available commands, can create custom slash commands, go to Integrations > Slash command
**Key points missing:** custom commands can call APIs, external users cannot access Integrations

#### Q17: How can I connect external applications to kChat?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> To connect external applications to kChat, you can use webhooks. Here’s how you can do it:

### Steps to Connect External Applications to kChat:

1. **Access the kChat Webhooks Interface**:
   - Open the **kChat** web app or desktop app.
   - Click on the **New** icon next to your kChat organization's name.
   - Select **Integrations**.
   - Choose the category **Incoming Webhooks**.

2. **Create an Incoming Webhook**:
   - Click on the blue button **Add incoming webhooks**.
   - Add a name and ...

**Key points found:** use webhooks, Incoming webhooks receive from external apps, Outgoing webhooks send to external apps, POST request with JSON text field, external users cannot access Integrations
**Key points missing:** Integrations menu

#### Q18: How do I translate a message in kChat?

**Rating:** [~] Partial (60.0% coverage)

**Response excerpt:**
> To translate a message in kChat, follow these steps:

1. Open the **kChat** web app, mobile app, or desktop app.
2. View the message you want to translate.
3. Click on the action menu (**•••**) located at the top right of the message.
4. Select **Translate**.
5. The translated message will appear below the conversation and will only be visible to you.

Source: [Translate the content of a message on the kChat Infomaniak app](https://www.infomaniak.com/en/support/faq/1467/translate-the-content-of-...

**Key points found:** click action menu (three dots) on message, click Translate, only visible to you
**Key points missing:** translation appears below, translates to your language

#### Q19: How can I invite external users to kChat?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To invite external users to kChat, follow these steps:

1. **Access kChat**:
   - Open the [kChat Web app](https://ksuite.infomaniak.com/kchat) or the kChat desktop app.

2. **Invite Members**:
   - Click the **Invite members** button.

3. **Invite a New User**:
   - Click the link to invite a new user.

4. **Specify Details**:
   - Enter the email address(es) of the person(s) you want to invite.
   - Specify the channel(s) to which these users will have access.

5. **Send the Invitation**:
   -...

**Key points found:** click Invite members, enter email and specify channels, users receive email invitation, external users not counted as users
**Key points missing:** must be Organization administrator, guests have limited permissions

#### Q20: What is Euria and how do I use it in kChat?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> ### What is Euria?
Euria is an artificial intelligence integrated into Infomaniak's kSuite, designed to assist with tasks such as calculations, translations, providing information, and answering questions. It is particularly useful as a conversational agent in kChat and for summarizing discussions.

### How to Use Euria in kChat:
1. **Add Euria to Your Contacts**:
   - Euria is already available as a bot in your kChat contacts.
   - If you don’t see it, click on the channel search or the **+** i...

**Key points found:** Euria is AI assistant in kSuite, calculations, translations, information, search for bot in channel search, create private discussion with bot
**Key points missing:** do not create group conversation, new users get welcome message

---

## Recommendations

- **Good coverage achieved.** Focus on:
  - Response latency optimization
  - Edge case handling