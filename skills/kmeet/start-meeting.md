---
name: start-meeting
description: Use when user asks to "start a meeting", "call someone", "video chat with", or "schedule a video call"
allowed-tools:
  - updateState
  - queryDB
  - showPanel
  - navigate
  - toast
trigger-phrases:
  - start a meeting
  - call someone
  - video chat
  - schedule a call
  - create a meeting
---

# Start Meeting

## Goal
Create and start a video meeting with specified participants.

## Procedure

1. **Parse participant information**
   - Extract names or email addresses from the user request
   - If no participants specified, ask for clarification

2. **Look up participants**
   - Use `queryDB` to find user records for mentioned participants
   - Verify that all participants exist in the system

3. **Create the meeting**
   - Use `updateState` to create a new meeting with:
     - Auto-generated meeting ID
     - Current user as host
     - Specified participants as invitees
     - Meeting status: "starting"

4. **Show meeting UI**
   - Use `showPanel` to display the meeting panel with:
     - Participant list
     - Meeting controls (mute, camera, share screen)
     - Meeting link for sharing

5. **Navigate to meeting**
   - Use `navigate` to switch to the kMeet application view
   - Focus on the newly created meeting

6. **Notify user**
   - Use `toast` to show success message: "Meeting started"
   - Include meeting link in the notification

## Error Handling

- If participant not found: Show toast with error and suggest checking the name
- If meeting creation fails: Show error panel with retry option
- If user cancels: Clean up any partial state

## Example User Requests

- "Start a meeting with Alice"
- "Call Bob and Carol"
- "Video chat with the marketing team"
- "I need to meet with Jean-Paul about the project"
