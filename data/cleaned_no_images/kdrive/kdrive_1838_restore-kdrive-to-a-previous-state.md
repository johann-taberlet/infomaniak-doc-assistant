# Restore k Drive to a previous state

Source: https://www.infomaniak.com/en/support/faq/1838/restore-kdrive-to-a-previous-state

---

This guide explains how to revert the file organization in your [k Drive](https://infomaniak.com/gtl/kdrive), especially if changes have been made and you have lost track.

**⚠ Available with:**

### Preamble

- The restore or *Rewind* feature allows you to revert to a previous state, like a time machine, and restore the order of your chosen files or your entire k Drive up to 3 months back (linked to the [file version retention period](https://www.infomaniak.com/en/support/faq/2384)).
- Files permanently deleted from your k Drive trash and deleted file versions **cannot be restored**.
- Restoration may take **several minutes**, during which **k Drive will be inaccessible** for all users, depending on the volume of data to be recovered.
- No actions are performed on permissions and shares.

## Access the k Drive restore tool

### Prerequisites

- Be [Administratoror Legal Representative](https://www.infomaniak.com/en/support/faq/1633) within the Organization.

To open the restore interface:

1. [Click here](https://ksuite.infomaniak.com/kdrive) to access the Infomaniak **k Drive** web app (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. Click on the **Settings** icon in the top right corner.
3. Check or select the relevant k Drive in the dropdown menu of the left sidebar.
4. Click on **Restore**:

5. Read the on-screen information, then click the button to **start**:

6. Review the information in the modal that appears, then click the button to **validate**.
7. Choose what will be affected by the rollback (the entire k Drive or just a part, and if applicable, for which user).
8. Click on **Continue**:

9. Choose the date to revert to (maximum 3 months / 90 days).
10. Click on **Continue**:

11. **Launch the analysis in the next step**, and determine the next steps based on the proposed result (and if a rollback yields no results, the analysis will indicate this):

12. A final security request will appear before the restoration begins.

After the operation, an email is sent, and a notification is displayed on the online k Drive.

## Analysis Report

An administrator viewing a report of a restoration initiated by another administrator will not see everything related to the personal folder of the administrator who started the restoration:

In the analysis report view, the data is listed and grouped by its current location before the rollback.

## In case of conflict

At the root of the k Drive of the administrator who performed the operation (or for the affected user) a folder named 'Restoration (date and time)' will be created, containing a subfolder with conflicting files called '**Conflict**' and another folder for the files currently in the target called '**Later Items**':