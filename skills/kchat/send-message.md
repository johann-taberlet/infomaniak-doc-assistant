---
name: send-message
description: Use when user asks to "send a message", "message someone", "chat with", or "tell someone"
allowed-tools:
  - updateState
  - queryDB
  - navigate
  - toast
trigger-phrases:
  - send a message
  - message someone
  - chat with
  - tell them
  - write to
---

# Send Message

## Goal
Send a chat message to a user or channel in kChat.

## Procedure

1. **Identify recipient**
   - Use `queryDB` to find user or channel
   - Handle both direct messages and channel messages

2. **Compose and send**
   - Use `updateState` to add message to conversation
   - Mark conversation as having new activity

3. **Navigate to chat**
   - Use `navigate` to open kChat view
   - Focus on the relevant conversation

4. **Confirm delivery**
   - Use `toast` to show "Message sent" notification

## Error Handling

- Recipient not found: Ask for clarification
- Channel access denied: Explain user is not a member
