@echo off
:: Проверяем, затребована ли справка или аргументы отсутствуют
if "%~1"=="" goto :help
if "%~1"=="?" goto :help
if "%~1"=="/?" goto :help
if "%~1"=="--help" goto :help
if "%~1"=="-h" goto :help

:: Парсим строку вида ip:port:login:password
for /f "tokens=1,2,3,4 delims=:" %%a in ("%~1") do (
    set "P_IP=%%a"
    set "P_PORT=%%b"
    set "P_USER=%%c"
    set "P_PASS=%%d"
)

:: Собираем URL для прокси
set "PROXY_URL=http://%P_USER%:%P_PASS%@%P_IP%:%P_PORT%"

:: Устанавливаем переменные окружения
set "HTTP_PROXY=%PROXY_URL%"
set "HTTPS_PROXY=%PROXY_URL%"

:: Выделяем команду для запуска
for /f "tokens=1,* delims= " %%a in ("%*") do set "CMD_LINE=%%b"

:: Если команды нет, выводим текущий конфиг
if "%CMD_LINE%"=="" (
    echo Proxy Env Vars prepared:
    echo %PROXY_URL%
    echo.
    echo Tip: Use 'px ?' for examples.
    exit /b
)

:: Запускаем переданную команду
echo [Proxy Active] Running: %CMD_LINE%
%CMD_LINE%
exit /b

:help
echo ======================================================
echo PX: Proxy Wrapper for Commands
echo ======================================================
echo Usage:
echo   px IP:PORT:LOGIN:PASS [command]
echo.
echo Examples:
echo   1. Check IP via curl:
echo      px 1.2.3.4:8080:user:pass curl ifconfig.me
echo.
echo   2. Install python packages:
echo      px 1.2.3.4:8080:user:pass pip install requests
echo.
echo   3. Run poetry commands:
echo      px 1.2.3.4:8080:user:pass poetry update
echo.
echo   4. Set vars for current session only (no command):
echo      px 1.2.3.4:8080:user:pass
echo.
echo Note: If your password contains special chars (like ^&), 
echo wrap the whole proxy string in double quotes:
echo   px "1.2.3.4:80:user:p@ss&word" command
echo ======================================================
exit /b