@echo off
set "flags="
set "targets="

:parse
if "%~1"=="" goto run
set "arg=%~1"
if "!arg!"=="-rf" (
    set "flags=-Recurse -Force"
) else if "!arg!"=="-r" (
    set "flags=-Recurse"
) else if "!arg!"=="-f" (
    set "flags=-Force"
) else (
    set "targets=%targets% '%~1'"
)
shift
goto parse

:run
if "%targets%"=="" (
    echo Usage: rm [-rf] target
    exit /b 1
)
powershell -NoProfile -Command "Remove-Item %targets% %flags%"
