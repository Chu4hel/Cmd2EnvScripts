@echo off
rem Алиас для ls в стиле Linux с использованием PowerShell
if "%~1"=="" (
    powershell -NoProfile -Command "Get-ChildItem | Sort-Object Name"
    exit /b
)

if "%~1"=="-laX" (
    powershell -NoProfile -Command "Get-ChildItem -Force | Sort-Object Extension, Name"
    exit /b
)

if "%~1"=="-la" (
    powershell -NoProfile -Command "Get-ChildItem -Force | Sort-Object Name"
    exit /b
)

if "%~1"=="-l" (
    powershell -NoProfile -Command "Get-ChildItem | Sort-Object Name"
    exit /b
)

rem Для всех остальных случаев просто передаем аргументы в dir или Get-ChildItem
powershell -NoProfile -Command "Get-ChildItem %*"
