@echo off
setlocal enabledelayedexpansion

REM Define the Downloads directory (update if needed)
set "DOWNLOADS_DIR=%USERPROFILE%\Downloads"

REM Change to the Downloads directory
cd /d "%DOWNLOADS_DIR%"

REM Loop through each file in the Downloads directory
for %%f in (*.*) do (
    REM Check if the item is a file
    if not exist "%%f\" (
        REM Get the file extension
        set "ext=%%~xf"
        REM Remove the leading dot from the extension
        set "ext=!ext:~1!"
        REM Check if the extension folder exists
        if not exist "!ext!" (
            mkdir "!ext!"
        )
        REM Move the file to the corresponding extension folder
        move "%%f" "!ext!\"
    )
)

REM End the script
endlocal
echo Organization complete.
pause
