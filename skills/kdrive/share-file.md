---
name: share-file
description: Use when user asks to "share a file", "send a document", "give access to", or "share with"
allowed-tools:
  - updateState
  - queryDB
  - showPanel
  - toast
trigger-phrases:
  - share a file
  - send a document
  - give access to
  - share with
  - share the file
---

# Share File

## Goal
Share a file or folder from kDrive with specified users or generate a public link.

## Procedure

1. **Identify the file**
   - Use `queryDB` to search for the file by name
   - If multiple matches, use `showPanel` to let user choose

2. **Determine sharing method**
   - If specific users mentioned: prepare user sharing
   - If "anyone" or "public": prepare link sharing

3. **Apply sharing settings**
   - Use `updateState` to update file permissions
   - Set appropriate access level (view, edit, download)

4. **Confirm success**
   - Use `toast` to notify user of successful share
   - If link created, include copy-to-clipboard option

## Error Handling

- File not found: Ask user to specify exact name or path
- User not found: Suggest checking email/username
- Permission denied: Explain user lacks sharing rights
