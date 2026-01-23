# Import Google Photos to k Drive

Source: https://www.infomaniak.com/en/support/faq/2540/import-google-photos-to-kdrive

---

This guide details how to import your photos from **Google Photos** (*https://photos.google.com/*) to [k Drive](https://infomaniak.com/gtl/kdrive) Infomaniak.

## 1. Export your Google photos

To retrieve all your photos stored on **Google Photos** on your computer's hard drive, you need to use the **Google Takeout** service. This allows you to choose which albums to retrieve if you want to proceed in steps:

1. Log in to [Google Takeout](https://takeout.google.com/).
2. Deselect all products to keep only **Google Photos**:

![image](https://faq.storage5.infomaniak.com/16ccd22b4306733854711e437c8ba36f6b393a19.png)

3. If necessary, deselect the albums not to export:

![image](https://faq.storage5.infomaniak.com/428524420408a0b4f4a475f4f3a79e4775146e44.png)

4. Move on to the next step at the bottom of the page:

![image](https://faq.storage5.infomaniak.com/9c67dede74eb6c276f8957c0c563b241e09fb443.png)

5. Configure the export by ZIP archives.
6. Click at the bottom on the “Create an export” button to start the export:

![image](https://faq.storage5.infomaniak.com/18c7fce035152188d39c8bd648b1b6d5658bb3da.png)

7. Wait (several hours or even several days) until you receive an email containing the links to the ZIP exports.
8. Download and then decompress the content on your computer:

![image](https://faq.storage5.infomaniak.com/9053fd65956caba39aca9202c1fbee9a940ff6d0.png)

9. Clean and merge your different photo folders if necessary.

## 2. Correct the dates of the exported photos…

During the export, the creation dates of the files are modified and replaced by the **export date** instead of the **original date of capture**. You must therefore correct the dates via an appropriate script.

Here is a script **for advanced users** that allows you to restore the correct data to your files from the EXIF information (it is recommended to process batches of 7000-8000 photos max. to avoid a crash):

### … on macOS

1. Download **Exif Tool** [https://exiftool.org/index.html](https://exiftool.org/index.html) (macOS Package).
2. Install the application by authorizing its opening beforehand if necessary:

![image](https://faq.storage5.infomaniak.com/4bde814ec3dd386703168d5de00df78dbb76645a.png)

3. Open **Script Editor** (located in your Applications > Utilities folder):

![image](https://faq.storage5.infomaniak.com/5cf9450b9771055d3b75e9538d0542e95abf572e.png)

4. Click on **New document**.
5. Copy and paste the long script provided below into the Script Editor window.
6. Click on **Run** to start the script, a window opens:

![image](https://faq.storage5.infomaniak.com/f8611be5bb4ecc8b3abebd2b526800a054cdfba9.png)

7. Select the folder to analyze.
8. Let the script run, it will modify the dates or write the errors in a file `errors.txt` on the desktop.

The script to copy and paste entirely:

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

### … on Windows

1. Download **Exif Tool** [https://exiftool.org/index.html](https://exiftool.org/index.html) (Windows executable)
2. Place it in an accessible folder (for example `C:\Exif Tool`).
3. Rename `exiftool(-k).exe` to `exiftool.exe`.
4. Note its path (for example `C:\Exif Tool\exiftool.exe`). The script looks for the executable in C:\Exif Tool\exiftool.exe. If you place it elsewhere, you need to modify the second line of the script.
5. Copy and paste the long script provided below into a text file such as Notepad on your computer.
6. Modify if necessary the **path** specified in the file with the one noted in step 4.
7. Save it with the `.ps1` extension, for example `Update Exif Dates.ps1`.
8. Right-click on the `.ps1` file to **run it with Power Shell** (a command interpreter and script writing environment, pre-installed on modern versions of Windows).
9. Select the folder to analyze.
10. Let the script run, it will modify the dates or write the errors in a file `Date Error.txt` on the desktop.

> **Note:** Power Shell may block scripts. To allow their execution (if necessary), open Power Shell **as an administrator** and type `Set-Execution Policy Remote Signed -Scope Current User`.

The script to copy and paste entirely:

```
# === Configuration ===
$exif Tool Path = "C:\Exif Tool\exiftool.exe"
$desktop = [Environment]:: Get Folder Path("Desktop")
$log Found = Join-Path $desktop "Date Found.txt"
$log Error = Join-Path $desktop "Date Error.txt"

# === Folder Selection Dialog ===
Add-Type -Assembly Name System. Windows. Forms
$folder Browser = New-Object System. Windows. Forms. Folder Browser Dialog
$folder Browser. Description = "Select the folder to process"
if ($folder Browser. Show Dialog() -ne "OK") { exit }
$folder = $folder Browser. Selected Path

function Process-Folder {
    param ([string]$path)
    Get-Child Item -Path $path -Recurse -File | For Each-Object {
        $file = $_
        $file Path = $file. Full Name
        $file Name = $file. Name
        $has Date = $true

        # Try reading EXIF date
        $photo Raw = & $exif Tool Path -Date Time Original -S -n "$file Path"
        if (-not $photo Raw) { $photo Raw = & $exif Tool Path -Create Date -S -n "$file Path" }

        if ($photo Raw -match "\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}") {
            $photo Date = $matches[0]
            # Nettoyage de la date pour formatage (YYYYMMDDHHMM. SS)
            $date String = $photo Date -replace '[: ]', ''

            if ($date String. Length -ge 14) {
                $formatted Date = $date String. Substring(0, 12) + "." + $date String. Substring(12, 2)
                try {
                    $new Date = [datetime]:: Parse Exact($photo Date, "yyyy: MM:dd HH:mm:ss", $null)
                    [System. IO. File]:: Set Creation Time($file Path, $new Date)
                    [System. IO. File]:: Set Last Write Time($file Path, $new Date)
                    Add-Content -Path $log Found -Value "EXIF date set for: $file Name → $photo Date"
                } catch {
                    $has Date = $false
                }
            } else { $has Date = $false }
        } else { $has Date = $false }

        if (-not $has Date) {
            if ($file Name -match "-(\d{8})") {
                $name Date Raw = $matches[1] + "120000"
                try {
                    & $exif Tool Path "-datetimeoriginal=$($matches[1]) 12:00:00" "$file Path"
                    & $exif Tool Path "-createdate=$($matches[1]) 12:00:00" "$file Path"
                    $new Date = [datetime]:: Parse Exact($name Date Raw, "yyyyMMddHHmmss", $null)
                    [System. IO. File]:: Set Creation Time($file Path, $new Date)
                    [System. IO. File]:: Set Last Write Time($file Path, $new Date)
                    Add-Content -Path $log Found -Value "Date from filename set for: $file Name"
                } catch {
                    Add-Content -Path $log Error -Value "Invalid date in filename: $file Name"
                }
            } else {
                Add-Content -Path $log Error -Value "No valid date found for: $file Name"
            }
        }
    }
}

# Execute processing
Process-Folder -path $folder
[System. Windows. Forms. Message Box]:: Show("Done! All files processed.")
```

## 3. Import photos to k Drive

> **Note:** Do not change your passwords until the import is complete.

Once your photos are ready, if their number is not too large (a few thousand items) and your Internet connection is suitable, you can simply open the Web app **k Drive** (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) and choose to import the folder containing your photos to the desired location:

1. [Click here](https://kdrive.infomaniak.com) to access the Web app **k Drive** Infomaniak (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. Navigate to the location where your photos will be stored.
3. Click the **New** button in the top left corner.
4. Click on **Import a folder**
5. Select the folder containing your photos on your computer.
6. Wait until your data is fully imported (the activity log scrolls at the bottom right):

![image](https://faq.storage5.infomaniak.com/05c4c3f4449357d5c804b714602ee2c56f58faee.png)

Otherwise, if you are synchronizing your data using the desktop app, simply place your photos in the folder structure of your k Drive folder on your computer. Synchronization will begin, and your photos will be securely sent to the Infomaniak servers.

## 4. Access your photos from your devices

You can now access your photos on your various devices connected to k Drive (until they synchronize if it is the k Drive desktop app).

- On the Web app **k Drive** Infomaniak (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) you can modify the presentation to better view your photos with an enlarged display of thumbnails:

![image](https://faq.storage5.infomaniak.com/288825a5898ef1b068f9a02a0efce7a37a82916a.png)