@echo off
if "%~1"=="" (
    echo Usage: touch filename
    exit /b 1
)
powershell -NoProfile -Command "if (!(Test-Path '%~1')) { New-Item -ItemType File -Path '%~1' | Out-Null } else { (Get-Item '%~1').LastWriteTime = Get-Date }"
