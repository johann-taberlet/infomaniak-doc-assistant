# Import data from k Drive from i Cloud

Source: https://www.infomaniak.com/en/support/faq/2515/import-data-from-kdrive-from-icloud

---

This guide details how to import **i Cloud** data using **r Clone** on [k Drive](https://infomaniak.com/gtl/kdrive) Infomaniak.

**⚠ Available with:**

### Preamble

- Since Apple does not offer an API like its competitors, a solution to retrieve documents from an i Cloud Drive is to install the [k Drive macOS app](https://www.infomaniak.com/en/support/faq/2374) to synchronize the icloud folder which must be in your library. The guide below offers a solid alternative.
- k Drive supports [rclone streaming upload](https://rclone.org/overview/#optional-features) via WebDAV, up to 50 Go (extendable to 100 Go) to avoid abuse, with automatic error management if the limit is exceeded without prior specification of the size via `Content-Length`.

## 1. Configure rclone for drive access

### Install rclone on your computer

There is a version of *rclone* with a graphical interface ([GUI](https://rclone.org/gui/)) but it is quite possible to do this via the command line (CLI):

1. Install *rclone* from a `Terminal`-type application on your device, by typing the entire following command:
`sudo -v ; curl https://rclone.org/install.sh | sudo bash`
2. Enter the password for your session on your computer to start the installation:

Refer to the official installation guide if necessary.

### Configure the remote disk (i Cloud) on rclone

1. Once *rclone* is installed, enter the command `rclone config`. Refer to the official configuration guide if necessary.
2. Then choose to configure a new remote import by answering `n` for `New remote`.
3. Name the remote disk, for example `appledrive`:

4. Then choose the type of disk to import by answering `iclouddrive` which corresponds to **i Cloud Drive** among the proposed choices.
5. Indicate to *rclone* the `apple_id` by entering your Apple ID (usually an email address).
6. Choose to use your own password linked to the Apple ID account (`y`).
7. Enter your password twice as requested:

8. Answer “No” `n` to the question about “advanced configuration”.
9. A window on your device should open to warn you of a remote connection; authorize it:

10. A window on your device should open with a 2FA code; copy it:

11. Paste the code when *rclone* asks for it.
12. Answer “Yes” `y` to the last question if all the presented information is correct.

### Configuration of the destination disk (k Drive) on rclone

It is possible to act directly on [the configuration file ofrclone](https://rclone.org/commands/rclone_config_file/) by pasting your k Drive configuration in it in the form for example:

```
[k Drive]
type = webdav
url = https://k Drive_ID_HERE.connect.kdrive.infomaniak.com/
vendor = other
user = user@email.com
pass = PASSWORD_HERE_OR_APP_PASSWORD_IF_2FA
```

But here is how to proceed step by step as for the previous configuration:

1. Still in the terminal, enter `n` for a new disk configuration and enter the name `k Drive` to recognize your destination disk:

2. Then choose the type of disk to import by answering `webdav` which corresponds to a WebDAV configuration among the proposed choices.
3. Enter the following information:url = direct access to k Drive (refer to this other guide regarding the k Drive ID for the connection URL)vendor = rclone (option #6)user = email address to log in to the Infomaniak user account
4. Answer “Yes” `y` to the password question, then enter the password:application password in case of double authentication activated or the one from your Infomaniak user account if you have not activated 2FA.
5. Leave the `bearer_token` blank, then answer “No” `n` to the question about “advanced configuration”.
6. Answer “Yes” `y` to the last question and your 2 disks will be displayed:

## 2. Copy data from i Cloud to k Drive

### Prerequisites

- Consult the available options in the [official guide](https://rclone.org/iclouddrive/) before starting an import.

Example of a command to start copying your i Cloud data to the root of your k Drive:

```
sudo rclone copy appledrive: k Drive:
```

This will immediately start copying your i Cloud folders, subfolders, and contents to the **personal folder** of your Infomaniak k Drive!

### Details about the dates of your exported photos

If you export your photos from i Cloud to Infomaniak k Drive, be vigilant about the date metadata. During export, the file creation dates may be modified and replaced by the export date instead of the original photo date.

Here is a script **for advanced users** that allows you to restore the correct data to your files from the EXIF information (it is recommended to process batches of 7000 photos max. to avoid a crash):

1. Download **Exif Tool** [https://exiftool.org/index.html](https://exiftool.org/index.html) (macOS Package).
2. Install the application by authorizing its opening in advance if necessary:

3. Open **Script Editor**(located in your Applications > Utilities folder):

4. Click on **New Document**.
5. Copy and paste the long script provided below into the Script Editor window.
6. Click on **Run** to start the script, a window opens:

7. Select the folder to analyze.
8. Let the script run afterwards, it will modify the dates or write the errors in a `errors.txt` file on the desktop.

The script to copy-paste entirely:

```
-- replace file date with EXIF creation date or date from name after the first dash -

tell application "Finder"
    set Folder Path to choose folder with prompt "Select the folder containing the files to update"
    my process Folder(Folder Path)
end tell

on process Folder(a Folder)
    tell application "Finder"
        -- process files:
        set file List to files of a Folder
        repeat with each File in file List
            -- process a single file

            set the File to each File
            set Apple Script's text item delimiters to {""}
            set file Name to name of each File --get the file name

            set each File to each File as string --file path
            set has Date to true --initialize date found flag

            try
                --get date if available
                set photo Date to do shell script "/usr/local/bin/exiftool -Date Time Original " & quoted form of POSIX path of each File
                if photo Date is "" then set photo Date to do shell script "/usr/local/bin/exiftool -Creation Date " & quoted form of POSIX path of each File
                if photo Date is "" then set photo Date to do shell script "/usr/local/bin/exiftool -Create Date " & quoted form of POSIX path of each File

                if photo Date is "" then
                    set has Date to false --check if date was found
                end if

            on error
                set has Date to false -- error retrieving date
                set photo Date to ""
            end try

            if length of photo Date > 20 then
                --format extracted date
                set x to (length of photo Date) - 33
                set Original Date to text -x thru -1 of photo Date
                set formatted Date to text 1 thru 5 of Original Date
                set the Year to formatted Date
                set formatted Date to formatted Date & text 7 thru 8 of Original Date
                set the Month to text 7 thru 8 of Original Date
                set formatted Date to formatted Date & text 10 thru 11 of Original Date
                set the Day to text 10 thru 11 of Original Date
                set formatted Date to formatted Date & text 13 thru 14 of Original Date
                set the Hour to text 13 thru 14 of Original Date
                set formatted Date to formatted Date & text 16 thru 17 of Original Date
                set the Minute to text 16 thru 17 of Original Date
                set formatted Date to formatted Date & "." & text 19 thru 20 of Original Date
                set the Second to text 19 thru 20 of Original Date
                set new Name to the Year & "-" & the Month & "-" & the Day & " " & the Hour & "." & the Minute & "." & the Second

                set test Value to formatted Date as string --check if found date is 000
                if test Value is " 000000000000.00" then
                    set has Date to false
                else
                    -- set file date to original EXIF date and write to log
                    do shell script "touch -t " & formatted Date & " " & quoted form of POSIX path of each File
                    set log File to open for access ((path to desktop folder as text) & "Date Found.txt") as text with write permission
                    write "Original date found for file: " & Original Date & " " & each File & return to log File starting at eof
                    close access log File
                end if
            end if

            if has Date is false then
                -- get date from file name after first dash
                set nb to ""
                set name Date to ""
                set file Name to file Name as string
                set saved Delimiters to Apple Script's text item delimiters --save delimiters
                set Apple Script's text item delimiters to {"-"} --split on "-"
                set nb to offset of "-" in file Name
                if nb is not 0 then
                    set Apple Script's text item delimiters to saved Delimiters --restore delimiters
                    set name Date to characters (nb + 1) thru (nb + 8) of file Name as string
                    set name Date to name Date & "1200.00"
                    set cmd1 to "/usr/local/bin/exiftool -datetimeoriginal=" & name Date & " " & quoted form of POSIX path of each File
                    set cmd2 to "/usr/local/bin/exiftool -createdate=" & name Date & " " & quoted form of POSIX path of each File
                end if
                try
                    -- write date from name to EXIF
                    do shell script cmd1
                    do shell script cmd2
                    do shell script "touch -t " & name Date & " " & quoted form of POSIX path of each File
                    do shell script "rm " & quoted form of POSIX path of (each File & "_original")
                on error
                    -- if date from name is invalid, log the error
                    set log File to open for access ((path to desktop folder as text) & "Date Error.txt") as text with write permission
                    write "No valid date found in file name: " & each File & return to log File starting at eof
                    close access log File
                end try
            end if
        end repeat

        -- process folders:
        set folder List to folders of a Folder
        repeat with each Subfolder in folder List
            -- process a subfolder
            my process Folder(each Subfolder)
        end repeat
    end tell
end process Folder

tell application "Finder"
    display dialog "Done! All files processed." buttons {"Close"}
end tell
```