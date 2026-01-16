# Import Google Photos to kDrive

Source: https://www.infomaniak.com/en/support/faq/2540/import-google-photos-to-kdrive

---

This guide details how to import your photos from **Google Photos** (*https://photos.google.com/*) to [kDrive](https://infomaniak.com/gtl/kdrive) Infomaniak.

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

1. Download **ExifTool** [https://exiftool.org/index.html](https://exiftool.org/index.html) (macOS Package).
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

### … on Windows

1. Download **ExifTool** [https://exiftool.org/index.html](https://exiftool.org/index.html) (Windows executable)
2. Place it in an accessible folder (for example `C:\ExifTool`).
3. Rename `exiftool(-k).exe` to `exiftool.exe`.
4. Note its path (for example `C:\ExifTool\exiftool.exe`).The script looks for the executable in C:\ExifTool\exiftool.exe. If you place it elsewhere, you need to modify the second line of the script.
5. Copy and paste the long script provided below into a text file such as Notepad on your computer.
6. Modify if necessary the **path** specified in the file with the one noted in step 4.
7. Save it with the `.ps1` extension, for example `UpdateExifDates.ps1`.
8. Right-click on the `.ps1` file to **run it with PowerShell** (a command interpreter and script writing environment, pre-installed on modern versions of Windows).
9. Select the folder to analyze.
10. Let the script run, it will modify the dates or write the errors in a file `DateError.txt` on the desktop.

> **Note:** PowerShell may block scripts. To allow their execution (if necessary), open PowerShell **as an administrator** and type `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.

The script to copy and paste entirely:

```
# === Configuration ===
$exifToolPath = "C:\ExifTool\exiftool.exe"
$desktop = [Environment]::GetFolderPath("Desktop")
$logFound = Join-Path $desktop "DateFound.txt"
$logError = Join-Path $desktop "DateError.txt"

# === Folder Selection Dialog ===
Add-Type -AssemblyName System.Windows.Forms
$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$folderBrowser.Description = "Select the folder to process"
if ($folderBrowser.ShowDialog() -ne "OK") { exit }
$folder = $folderBrowser.SelectedPath

function Process-Folder {
    param ([string]$path)
    Get-ChildItem -Path $path -Recurse -File | ForEach-Object {
        $file = $_
        $filePath = $file.FullName
        $fileName = $file.Name
        $hasDate = $true

        # Try reading EXIF date
        $photoRaw = & $exifToolPath -DateTimeOriginal -S -n "$filePath"
        if (-not $photoRaw) { $photoRaw = & $exifToolPath -CreateDate -S -n "$filePath" }
        
        if ($photoRaw -match "\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}") {
            $photoDate = $matches[0]
            # Nettoyage de la date pour formatage (YYYYMMDDHHMM.SS)
            $dateString = $photoDate -replace '[: ]', ''
            
            if ($dateString.Length -ge 14) {
                $formattedDate = $dateString.Substring(0, 12) + "." + $dateString.Substring(12, 2)
                try {
                    $newDate = [datetime]::ParseExact($photoDate, "yyyy:MM:dd HH:mm:ss", $null)
                    [System.IO.File]::SetCreationTime($filePath, $newDate)
                    [System.IO.File]::SetLastWriteTime($filePath, $newDate)
                    Add-Content -Path $logFound -Value "EXIF date set for: $fileName → $photoDate"
                } catch {
                    $hasDate = $false
                }
            } else { $hasDate = $false }
        } else { $hasDate = $false }

        if (-not $hasDate) {
            if ($fileName -match "-(\d{8})") {
                $nameDateRaw = $matches[1] + "120000"
                try {
                    & $exifToolPath "-datetimeoriginal=$($matches[1]) 12:00:00" "$filePath"
                    & $exifToolPath "-createdate=$($matches[1]) 12:00:00" "$filePath"
                    $newDate = [datetime]::ParseExact($nameDateRaw, "yyyyMMddHHmmss", $null)
                    [System.IO.File]::SetCreationTime($filePath, $newDate)
                    [System.IO.File]::SetLastWriteTime($filePath, $newDate)
                    Add-Content -Path $logFound -Value "Date from filename set for: $fileName"
                } catch {
                    Add-Content -Path $logError -Value "Invalid date in filename: $fileName"
                }
            } else {
                Add-Content -Path $logError -Value "No valid date found for: $fileName"
            }
        }
    }
}

# Execute processing
Process-Folder -path $folder
[System.Windows.Forms.MessageBox]::Show("Done! All files processed.")
```

## 3. Import photos to kDrive

> **Note:** Do not change your passwords until the import is complete.

Once your photos are ready, if their number is not too large (a few thousand items) and your Internet connection is suitable, you can simply open the Web app **kDrive** (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) and choose to import the folder containing your photos to the desired location:

1. [Click here](https://kdrive.infomaniak.com) to access the Web app **kDrive** Infomaniak (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)).
2. Navigate to the location where your photos will be stored.
3. Click the **New** button in the top left corner.
4. Click on **Import a folder**
5. Select the folder containing your photos on your computer.
6. Wait until your data is fully imported (the activity log scrolls at the bottom right):

![image](https://faq.storage5.infomaniak.com/05c4c3f4449357d5c804b714602ee2c56f58faee.png)

Otherwise, if you are synchronizing your data using the desktop app, simply place your photos in the folder structure of your kDrive folder on your computer. Synchronization will begin, and your photos will be securely sent to the Infomaniak servers.

## 4. Access your photos from your devices

You can now access your photos on your various devices connected to kDrive (until they synchronize if it is the kDrive desktop app).

- On the Web app **kDrive** Infomaniak (online service [ksuite.infomaniak.com/kdrive](https://ksuite.infomaniak.com/kdrive)) you can modify the presentation to better view your photos with an enlarged display of thumbnails:

![image](https://faq.storage5.infomaniak.com/288825a5898ef1b068f9a02a0efce7a37a82916a.png)