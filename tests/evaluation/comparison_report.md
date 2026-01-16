# RAG Quality Evaluation Report

**Generated:** 2026-01-16 12:50:59
**Questions Tested:** 20

---

## Summary Metrics

| Metric | Value |
|--------|-------|
| Total Score | 31/60 (51.7%) |
| Average Score | 1.55/3.00 |
| Average Coverage | 45.5% |
| Average Response Time | 37.0s |

## Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Complete (3) | 5 | 25.0% |
| Partial (2) | 5 | 25.0% |
| Minimal (1) | 6 | 30.0% |
| Wrong (0) | 4 | 20.0% |

---

## Detailed Results

### kMeet (7 questions)

#### Q1: How do I create a kMeet meeting?

**Rating:** [~] Partial (60.0% coverage)

**Response excerpt:**
> To create a **kMeet meeting**, follow these steps:

### **Basic Steps**
1. **Access kMeet**:
   - Open [kmeet.infomaniak.com](https://kmeet.infomaniak.com) in your browser or use the kMeet app on your device (macOS, Windows, Linux, iOS, Android).
2. **Start a New Meeting**:
   - Click "Start a new meeting" or similar option.  
   *(Source: [Create a kMeet meeting](https://www.infomaniak.com/en/support/faq/2475))*  

---

### **Advanced Options**
- **Secure the Meeting**:
  - Set a **password** a...

**Key points found:** kmeet.infomaniak.com, click Join the meeting, share room link
**Key points missing:** enter meeting room name, allow webcam/microphone access

#### Q2: How can I share my screen during a kMeet call?

**Rating:** [-] Minimal (40.0% coverage)

**Response excerpt:**
> To share your screen during a kMeet call, follow these steps:

- **During the call**:  
  1. Click the **screen share icon** (usually a screen with a "+" or a camera icon) in the controls.  
  2. Select the specific window, application, or entire screen you want to share.  
  3. Confirm the share settings (e.g., allow others to take control).  

- **Permissions**:  
  If using a browser, you may need to grant permission for screen sharing (e.g., click "Allow" when prompted).  

- **Mobile device...

**Key points found:** click screen icon with arrow, choose entire screen or specific window
**Key points missing:** not available on iOS, validate authorization, stop by clicking toolbar icon

#### Q3: What should I do if my audio is not working in kMeet?

**Rating:** [~] Partial (50.0% coverage)

**Response excerpt:**
> If your audio is not working in **kMeet**, follow these steps based on the Windows troubleshooting guide:

### ✅ Check Privacy Settings
1. Open **Windows Settings** > **Privacy**.
2. Ensure **"Allow apps to access the camera"** and **"Choose which Microsoft Store apps can access the camera"** are enabled.
3. Enable **Windows Search**, **Camera**, and **App Connector** (for microphone, repeat the same steps).

### 🛠️ Use Audio Troubleshooter
1. Click the **Search** icon in the taskbar, type **"Au...

**Key points found:** check Settings for microphone permission, mobile Privacy settings, Windows Audio Troubleshooter
**Key points missing:** browser lock icon, try different device, Firefox WebRTC disable option

#### Q4: How do I create side rooms (breakout rooms) in kMeet?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To create side rooms (breakout rooms) in **kMeet**, follow these steps:

- **Step 1:** Start a kMeet meeting as a **moderator** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or a supported app.  
- **Step 2:** While in the meeting, click the **multi-user icon** in the toolbar.  
- **Step 3:** Click the **"Add side room"** button to create one or more breakout rooms.  
- **Step 4:** Participants can join or leave side rooms using the same button (multi-user icon) to manage their sessio...

**Key points found:** click multi-user icon, add side room button, participants can join/leave, moderator can force participants to join
**Key points missing:** must be moderator

#### Q5: How can I record a kMeet meeting?

**Rating:** [+] Complete (85.7% coverage)

**Response excerpt:**
> To record a **kMeet meeting** on **kDrive**, follow these steps:

### 🎬 Record a kMeet Meeting on kDrive
1. **Start kMeet** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or your device app.
2. **Join a meeting** or create a new one.
3. Click the **action menu** (○○○) in the kMeet toolbar.
4. Select the **record icon** (◉) to start recording.
5. **Confirm the action**:
   - Log in to your Infomaniak account if prompted.
   - Choose a **kDrive folder** to save the recording.
6. Click **...

**Key points found:** must be moderator, click action menu (three dots), Start recording, saved to kDrive root, .mp4 format, max 3 hours
**Key points missing:** need kDrive

#### Q6: How do I set a password for my kMeet meeting?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To set a password for your kMeet meeting, follow these steps:

1. **Start kMeet** via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or your device app.
2. **Create a new meeting**:
   - Enter a name for your meeting room.
   - Click **Security options**.
   - Enable **Protect access** by toggling the switch.
   - Set your desired **password**.
   - Click **Continue** to start the meeting.
3. **Share details**: Distribute the **meeting link/code** and **password** to participants (you can ...

**Key points found:** click security options, enable Protect access toggle, create password, share link AND password
**Key points missing:** end-to-end encryption option available

#### Q7: How can I livestream a kMeet meeting?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To livestream a kMeet meeting, follow these steps based on the Infomaniak documentation:

### Steps to Broadcast a kMeet Meeting via Live Streaming
1. **Start a kMeet Meeting**  
   - Initiate a meeting via [kmeet.infomaniak.com](https://kmeet.infomaniak.com) or through the desktop/mobile app.  
   - Ensure all participants are connected before starting the stream.  

2. **Enable Live Streaming Mode**  
   - During the meeting, access the **meeting settings** (usually via a menu icon like ⚙️ or ...

**Key points found:** Start live broadcast, copy stream URL to share, max 24 hours, stops when meeting ends
**Key points missing:** must be moderator, click action menu

### kDrive (7 questions)

#### Q8: How do I install kDrive on Linux?

**Rating:** [x] Wrong (0.0% coverage)

**Response excerpt:**
> The installation instructions for kDrive on Linux are available in the provided documentation. Here's what you can do:

- Visit the official guide: [Install kDrive on Linux](https://www.infomaniak.com/en/support/faq/617/install-kdrive-on-linux) for detailed steps.
- If you need further assistance, contact [Infomaniak support](https://www.infomaniak.com/en/support) for help with specific issues during installation. 

Let me know if you need additional guidance!

**Key points missing:** .AppImage file, install libfuse2, right-click Permissions, Allow executing file as program, Ubuntu 22.04 LTS officially supported, Lite Sync not available on Linux

#### Q9: How can I share a file from kDrive?

**Rating:** [-] Minimal (33.3% coverage)

**Response excerpt:**
> To share a file from **kDrive**, follow these steps:

- **Step 1**: Navigate to the file you want to share in your kDrive storage.
- **Step 2**: Click the **"Share"** button (usually located near the file actions).
- **Step 3**: Enter the email addresses of the people you want to share the file with.
- **Step 4**: Set permission levels (e.g., **View**, **Edit**, or **Comment**).
- **Step 5**: Optionally, set an expiration date for the shared link or enable a password.
- **Step 6**: Send the invi...

**Key points found:** click Share, public share link option
**Key points missing:** right-click on file/folder, can set expiration, password, add users with viewing/modification/management rights, recipients can create free Infomaniak account

#### Q10: What is a Drop Box in kDrive and how do I create one?

**Rating:** [x] Wrong (0.0% coverage)

**Response excerpt:**
> The provided documentation does not contain information about a "Drop Box" feature in kDrive or steps to create one. These results relate to other topics like kDrive blocks, kChat invites, and screen sharing in kMeet. For details on Drop Box functionality, please contact Infomaniak support directly. 

No relevant sources found in the provided context.

**Key points missing:** invite contacts to deposit files, click New then Drop Box, enter name, can set password, expiration, storage limit, email notification option, disable converts to regular folder

#### Q11: How do I resolve sync conflicts in kDrive?

**Rating:** [-] Minimal (33.3% coverage)

**Response excerpt:**
> To resolve sync conflicts in kDrive, follow these steps:

- **Prevent conflicts** by:
  - Avoiding simultaneous edits on the same file (unless using collaborative tools like Word/Excel online).
  - Syncing offline changes before making online modifications.
  - Avoiding duplicate folder names across devices.  
  *(Source: [Avoid synchronization conflicts](https://www.infomaniak.com/en/support/faq/2403/resolve-a-kdrive-synchronization-conflict))*

- **Manual resolution** (if automatic fixes fail)...

**Key points found:** kDrive Web version is kept, kDrive Rescue Folder for protection
**Key points missing:** conflicts when same file modified locally and online, local saved as _conflict, can keep both, delete, or merge, view via kDrive icon > info

#### Q12: How do I manage user rights in kDrive?

**Rating:** [-] Minimal (40.0% coverage)

**Response excerpt:**
> To manage user rights in **kDrive**, follow these steps:

### Steps to Modify User Permissions:
1. **Access kDrive Web App**  
   Go to [https://ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive) (source: [FAQ 2365](https://www.infomaniak.com/en/support/faq/2365/manage-a-kdrive-users-rights)).

2. **Select the Relevant kDrive**  
   Use the dropdown menu in the left sidebar to choose the specific kDrive instance.

3. **Open User Management**  
   Click the **action menu ⋮** next...

**Key points found:** Administrator has full access, Manage users in action menu
**Key points missing:** Administrator vs User levels, User cannot manage product, don't confuse Manager rights with kDrive rights

#### Q13: How can I access kDrive files locally without downloading them?

**Rating:** [+] Complete (80.0% coverage)

**Response excerpt:**
> To access kDrive files locally without fully downloading them, use the **Lite Sync** feature (available on Windows):

### Steps:
- **Install the kDrive desktop app** (required for Lite Sync).  
- Enable **Lite Sync** in the app settings. This stores files in a "dehydrated" state on your device, reducing local storage usage.  
- Files are accessible via the **kDrive web app** (online service [kdrive.infomaniak.com](https://kdrive.infomaniak.com)), but locally they load on-demand when opened.  

*...

**Key points found:** install kDrive desktop app, Open kDrive Web for server files, or open local folder, Lite Sync for virtual files
**Key points missing:** click icon in notification area

#### Q14: How do I sync kDrive with my Synology NAS?

**Rating:** [-] Minimal (20.0% coverage)

**Response excerpt:**
> To sync kDrive with your Synology NAS, follow these steps:

- **Install Synology Drive App**: Ensure the Synology Drive app is installed on your NAS device. This app facilitates cloud storage integration. [Synology Drive Documentation](https://www.synology.com/en-us/dsm/DSM-Drive)
- **Configure Sync Folder**: Set up the folder on your NAS that you want to sync with kDrive. This is done via the Synology Drive app settings. [Synology Drive Setup Guide](https://www.synology.com/en-us/knowledgebase/...

**Key points found:** use Cloud Sync app
**Key points missing:** choose WebDAV, server: https://[kDriveID].connect.kdrive.infomaniak.com, use application password, Bidirectional, Download remote, or Download local sync

### kChat (6 questions)

#### Q15: How do I create a channel in kChat?

**Rating:** [x] Wrong (0.0% coverage)

**Response excerpt:**
> The provided documentation does not include specific steps for creating a channel in kChat. It focuses on managing existing channels (e.g., descriptions, headers, converting public/private channels, or organizing categories). 

For detailed instructions on creating a channel, please consult Infomaniak support or check the official kChat documentation directly. 

Source: [Manage a kChat channel](https://www.infomaniak.com/en/support/faq/2732/manage-a-kchat-channel)

**Key points missing:** click button in left sidebar, Create a new channel, set name, URL, private/public, description, General channel exists by default, can convert, leave, archive channels

#### Q16: What slash commands are available in kChat?

**Rating:** [+] Complete (83.3% coverage)

**Response excerpt:**
> The documentation mentions that kChat supports slash commands starting with `/`, but it does not provide a complete list of pre-defined commands. Here's what is known:

- **Basic commands**: Typing `/` alone shows a modal with options like "Go offline" (source: [kChat slash commands guide](https://www.infomaniak.com/en/support/faq/2134/using-kchat-slash-commands)).
- **Custom commands**: Users can create custom commands via the "Integrations" settings (requires technical setup, e.g., API calls o...

**Key points found:** type / followed by command, just / shows available commands, can create custom slash commands, go to Integrations > Slash command, custom commands can call APIs
**Key points missing:** external users cannot access Integrations

#### Q17: How can I connect external applications to kChat?

**Rating:** [~] Partial (50.0% coverage)

**Response excerpt:**
> To connect external applications to **kChat**, follow these steps based on the official documentation:

### Steps to Connect External Applications via Webhooks
1. **Ensure Prerequisites**  
   - You must **not** be an external user (external users cannot access the *Integrations* menu).  
   - Verify your account type and permissions.  

2. **Configure Webhooks**  
   - Navigate to the **Integrations** section in your kChat admin panel.  
   - Locate the option to add or configure webhooks for e...

**Key points found:** use webhooks, Integrations menu, external users cannot access Integrations
**Key points missing:** Incoming webhooks receive from external apps, Outgoing webhooks send to external apps, POST request with JSON text field

#### Q18: How do I translate a message in kChat?

**Rating:** [-] Minimal (40.0% coverage)

**Response excerpt:**
> To translate a message in kChat:

- Click on the **Translate** button within the message  
- The translated text will appear below the conversation and is only visible to you  

Source: [Translate a message in kChat](https://www.infomaniak.com/en/support/faq/1467/translate-the-content-of-a-message-on-the-kchat-infomaniak-app)

**Key points found:** click Translate, only visible to you
**Key points missing:** click action menu (three dots) on message, translation appears below, translates to your language

#### Q19: How can I invite external users to kChat?

**Rating:** [~] Partial (66.7% coverage)

**Response excerpt:**
> To invite external users to kChat, follow these methods based on your needs:

### **Method 1: Invite as a Non-kSuite User (Not Counted Toward License)**
- **Prerequisites**: You must be an administrator with full rights for kChat.
- **Steps**:
  1. Go to your Organization’s settings in kChat.
  2. Invite the external user via email.
  3. They will create an Infomaniak account if they don’t already have one.
  4. They gain access to kChat but are **not counted** as a kSuite user or part of your O...

**Key points found:** must be Organization administrator, click Invite members, enter email and specify channels, external users not counted as users
**Key points missing:** users receive email invitation, guests have limited permissions

#### Q20: What is Euria and how do I use it in kChat?

**Rating:** [x] Wrong (0.0% coverage)

**Response excerpt:**
> The provided documentation does not mention "Euria" or its integration with kChat. The available information covers kChat features like inviting users, connecting external applications via webhooks, and kDrive-related topics. For specifics on Euria, please contact Infomaniak support directly. 

No relevant sources found in the provided context.

**Key points missing:** Euria is AI assistant in kSuite, calculations, translations, information, search for bot in channel search, create private discussion with bot, do not create group conversation, new users get welcome message

---

## Root Cause Analysis

### Investigation Results

Manual investigation of the 4 "Wrong" responses revealed two distinct issues:

#### Issue 1: Embedding Model Limitations (Q10, Q20)
The `nomic-embed-text` model via Ollama struggles with:
- **Proper nouns**: "Euria" queries return completely irrelevant documents despite 13 Euria chunks existing
- **Question-style queries**: "What is a Drop Box?" fails, but "drop box kdrive" succeeds

| Query | Correct Doc Found? | Notes |
|-------|-------------------|-------|
| "What is a Drop Box in kDrive?" | No | Returns irrelevant docs |
| "drop box kdrive" | Yes (0.63) | Keyword match works |
| "What is Euria in kChat?" | No | Returns irrelevant docs |
| "euria kchat AI" | No | Even direct match fails |

#### Issue 2: Chunk Content vs Query Mismatch (Q8, Q15)
The correct documents ARE retrieved but:
- Q8 (Linux install): Retrieved doc has score 0.764 but LLM says "visit the official guide" instead of reading the content
- Q15 (kChat channel): Retrieved chunks contain channel management, not creation steps (chunking split the creation section)

### Documents in Qdrant
- Total chunks: 579
- Drop Box chunks: 13
- Euria chunks: 13
- Linux kDrive chunks: 18

All relevant content EXISTS but isn't being properly retrieved or utilized.

---

## Recommendations

### Quick Wins (for Demo)

1. **Increase RAG_TOP_K from 5 to 8-10**
   - More candidates = higher chance of relevant content
   - Trade-off: slightly more context for LLM

2. **Improve System Prompt**
   - Add instruction: "Always extract specific steps from the retrieved documentation"
   - Add: "Never say documentation doesn't contain info if documents were retrieved"

3. **Chunk Size Adjustment**
   - Current: 500 chars with 50 overlap
   - Consider: 800-1000 chars to keep procedures intact

### Medium-Term Improvements

1. **Hybrid Search**
   - Combine vector search with BM25 keyword search
   - Would fix "Euria" and "Drop Box" retrieval

2. **Query Expansion**
   - Reformulate questions as keyword queries before search
   - Example: "How do I create a channel?" → "kchat create channel steps"

3. **Better Embedding Model**
   - Consider `mxbai-embed-large` or OpenAI embeddings
   - Trade-off: API costs vs quality

### Performance Note
Average response time of 37s is high. Consider:
- Using a smaller/faster chat model
- Caching frequent queries
- Streaming responses (already implemented)