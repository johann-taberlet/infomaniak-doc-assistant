# Import data from kDrive from iCloud

Source: https://www.infomaniak.com/en/support/faq/2515/import-data-from-kdrive-from-icloud

---

This guide details how to import **iCloud** data using **rClone** on [kDrive](https://infomaniak.com/gtl/kdrive) Infomaniak.

**⚠ Available with:**

### Preamble

- Since Apple does not offer an API like its competitors, a solution to retrieve documents from an iCloud Drive is to install the [kDrive macOS app](https://www.infomaniak.com/en/support/faq/2374) to synchronize the icloud folder which must be in your library. The guide below offers a solid alternative.
- kDrive supports [rclone streaming upload](https://rclone.org/overview/#optional-features) via WebDAV, up to 50 Go (extendable to 100 Go) to avoid abuse, with automatic error management if the limit is exceeded without prior specification of the size via `Content-Length`.

## 1. Configure rclone for drive access

### Install rclone on your computer

There is a version of *rclone* with a graphical interface ([GUI](https://rclone.org/gui/)) but it is quite possible to do this via the command line (CLI):

1. Install *rclone* from a `Terminal`-type application on your device, by typing the entire following command:
`sudo -v ; curl https://rclone.org/install.sh | sudo bash`
2. Enter the password for your session on your computer to start the installation:

![image](https://faq.storage5.infomaniak.com/057eab83b978cc2c211fb6e87581b5f007abc083.png)
Refer to the official installation guide if necessary.

### Configure the remote disk (iCloud) on rclone

1. Once *rclone* is installed, enter the command `rclone config`.Refer to the official configuration guide if necessary.
2. Then choose to configure a new remote import by answering `n` for `New remote`.
3. Name the remote disk, for example `appledrive`:

![image](https://faq.storage5.infomaniak.com/02113c330daed83f3aac65ce0a7cb5c895d7bb3e.png)

4. Then choose the type of disk to import by answering `iclouddrive` which corresponds to **iCloud Drive** among the proposed choices.
5. Indicate to *rclone* the `apple_id` by entering your Apple ID (usually an email address).
6. Choose to use your own password linked to the Apple ID account (`y`).
7. Enter your password twice as requested:

![image](https://faq.storage5.infomaniak.com/4aba0af310eff969275a80278c1eb658371e87f4.png)

8. Answer “No” `n` to the question about “advanced configuration”.
9. A window on your device should open to warn you of a remote connection; authorize it:

![image](https://faq.storage5.infomaniak.com/40b7ff8e020250ba38e044f811e875397ad6ef14.png)

10. A window on your device should open with a 2FA code; copy it:

![image](https://faq.storage5.infomaniak.com/0844656dd33f3947b20c2800c685c30804419b13.png)

11. Paste the code when *rclone* asks for it.
12. Answer “Yes” `y` to the last question if all the presented information is correct.

### Configuration of the destination disk (kDrive) on rclone

It is possible to act directly on [the configuration file ofrclone](https://rclone.org/commands/rclone_config_file/) by pasting your kDrive configuration in it in the form for example:

```
[kDrive]
type = webdav
url = https://kDrive_ID_HERE.connect.kdrive.infomaniak.com/
vendor = other
user = user@email.com
pass = PASSWORD_HERE_OR_APP_PASSWORD_IF_2FA
```

But here is how to proceed step by step as for the previous configuration:

1. Still in the terminal, enter `n` for a new disk configuration and enter the name `kDrive` to recognize your destination disk:

![image](https://faq.storage5.infomaniak.com/c45e287f1cefae21077e9db45f450bfe1d4febaf.png)

2. Then choose the type of disk to import by answering `webdav` which corresponds to a WebDAV configuration among the proposed choices.
3. Enter the following information:url = direct access to kDrive (refer to this other guide regarding the kDrive ID for the connection URL)vendor = rclone (option #6)user = email address to log in to the Infomaniak user account
4. Answer “Yes” `y` to the password question, then enter the password:application password in case of double authentication activated or ‍the one from your Infomaniak user account if you have not activated 2FA.
5. Leave the `bearer_token` blank, then answer “No” `n` to the question about “advanced configuration”.
6. Answer “Yes” `y` to the last question and your 2 disks will be displayed:

![image](https://faq.storage5.infomaniak.com/e0f4bcfaa155c9992da7a2a95da6c05e75463c4a.png)
‍

## 2. Copy data from iCloud to kDrive

### Prerequisites

- Consult the available options in the [official guide](https://rclone.org/iclouddrive/) before starting an import.

Example of a command to start copying your iCloud data to the root of your kDrive:

```
sudo rclone copy appledrive: kDrive:
```

This will immediately start copying your iCloud folders, subfolders, and contents to the **personal folder** of your Infomaniak kDrive!

### Details about the dates of your exported photos

If you export your photos from iCloud to Infomaniak kDrive, be vigilant about the date metadata. During export, the file creation dates may be modified and replaced by the export date instead of the original photo date.

Here is a script **for advanced users** that allows you to restore the correct data to your files from the EXIF information (it is recommended to process batches of 7000 photos max. to avoid a crash):

1. Download **ExifTool** [https://exiftool.org/index.html](https://exiftool.org/index.html) (macOS Package).
2. Install the application by authorizing its opening in advance if necessary:

![image](https://faq.storage5.infomaniak.com/4bde814ec3dd386703168d5de00df78dbb76645a.png)

3. Open **Script Editor**(located in your Applications > Utilities folder):

![image](https://faq.storage5.infomaniak.com/5cf9450b9771055d3b75e9538d0542e95abf572e.png)

4. Click on **New Document**.
5. Copy and paste the long script provided below into the Script Editor window.
6. Click on **Run** to start the script, a window opens:

![image](https://faq.storage5.infomaniak.com/f8611be5bb4ecc8b3abebd2b526800a054cdfba9.png)

7. Select the folder to analyze.
8. Let the script run afterwards, it will modify the dates or write the errors in a `errors.txt` file on the desktop.

The script to copy-paste entirely:

```
-- replace file date with EXIF creation date or date from name after the first dash -

tell application "Finder"
    set FolderPath to choose folder with prompt "Select the folder containing the files to update"
    my processFolder(FolderPath)
end tell

on processFolder(aFolder)
    tell application "Finder"
        -- process files:
        set fileList to files of aFolder
        repeat with eachFile in fileList
            -- process a single file
            
            set theFile to eachFile
            set AppleScript's text item delimiters to {""}
            set fileName to name of eachFile --get the file name
            
            set eachFile to eachFile as string --file path
            set hasDate to true --initialize date found flag
            
            try
                --get date if available
                set photoDate to do shell script "/usr/local/bin/exiftool -DateTimeOriginal " & quoted form of POSIX path of eachFile
                if photoDate is "" then set photoDate to do shell script "/usr/local/bin/exiftool -CreationDate " & quoted form of POSIX path of eachFile
                if photoDate is "" then set photoDate to do shell script "/usr/local/bin/exiftool -CreateDate " & quoted form of POSIX path of eachFile
                
                if photoDate is "" then
                    set hasDate to false --check if date was found
                end if
                
            on error
                set hasDate to false -- error retrieving date
                set photoDate to ""
            end try
            
            if length of photoDate > 20 then
                --format extracted date
                set x to (length of photoDate) - 33
                set OriginalDate to text -x thru -1 of photoDate
                set formattedDate to text 1 thru 5 of OriginalDate
                set theYear to formattedDate
                set formattedDate to formattedDate & text 7 thru 8 of OriginalDate
                set theMonth to text 7 thru 8 of OriginalDate
                set formattedDate to formattedDate & text 10 thru 11 of OriginalDate
                set theDay to text 10 thru 11 of OriginalDate
                set formattedDate to formattedDate & text 13 thru 14 of OriginalDate
                set theHour to text 13 thru 14 of OriginalDate
                set formattedDate to formattedDate & text 16 thru 17 of OriginalDate
                set theMinute to text 16 thru 17 of OriginalDate
                set formattedDate to formattedDate & "." & text 19 thru 20 of OriginalDate
                set theSecond to text 19 thru 20 of OriginalDate
                set newName to theYear & "-" & theMonth & "-" & theDay & " " & theHour & "." & theMinute & "." & theSecond
                
                set testValue to formattedDate as string --check if found date is 000
                if testValue is " 000000000000.00" then
                    set hasDate to false
                else
                    -- set file date to original EXIF date and write to log
                    do shell script "touch -t " & formattedDate & " " & quoted form of POSIX path of eachFile
                    set logFile to open for access ((path to desktop folder as text) & "Date Found.txt") as text with write permission
                    write "Original date found for file: " & OriginalDate & " " & eachFile & return to logFile starting at eof
                    close access logFile
                end if
            end if
            
            if hasDate is false then
                -- get date from file name after first dash
                set nb to ""
                set nameDate to ""
                set fileName to fileName as string
                set savedDelimiters to AppleScript's text item delimiters --save delimiters
                set AppleScript's text item delimiters to {"-"} --split on "-"
                set nb to offset of "-" in fileName
                if nb is not 0 then
                    set AppleScript's text item delimiters to savedDelimiters --restore delimiters
                    set nameDate to characters (nb + 1) thru (nb + 8) of fileName as string
                    set nameDate to nameDate & "1200.00"
                    set cmd1 to "/usr/local/bin/exiftool -datetimeoriginal=" & nameDate & " " & quoted form of POSIX path of eachFile
                    set cmd2 to "/usr/local/bin/exiftool -createdate=" & nameDate & " " & quoted form of POSIX path of eachFile
                end if
                try
                    -- write date from name to EXIF
                    do shell script cmd1
                    do shell script cmd2
                    do shell script "touch -t " & nameDate & " " & quoted form of POSIX path of eachFile
                    do shell script "rm " & quoted form of POSIX path of (eachFile & "_original")
                on error
                    -- if date from name is invalid, log the error
                    set logFile to open for access ((path to desktop folder as text) & "Date Error.txt") as text with write permission
                    write "No valid date found in file name: " & eachFile & return to logFile starting at eof
                    close access logFile
                end try
            end if
        end repeat
        
        -- process folders:
        set folderList to folders of aFolder
        repeat with eachSubfolder in folderList
            -- process a subfolder
            my processFolder(eachSubfolder)
        end repeat
    end tell
end processFolder

tell application "Finder"
    display dialog "Done! All files processed." buttons {"Close"}
end tell
```