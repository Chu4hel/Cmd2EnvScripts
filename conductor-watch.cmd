@echo off
:: 1. Сохраняем путь к текущей папке
set "TARGET_PATH=%cd%"

:: 2. Переходим в директорию демона
cd /d "D:\PROJECTS\_conductor_daemon"

:: --- Очистка окружения ---
:: Удаляем следы активированного окружения из текущей сессии батника
set VIRTUAL_ENV=
set PYTHONHOME=
set PYTHONPATH=
:: -------------------------------

echo [i] Starting Conductor Daemon...
echo [i] Monitoring directory: %TARGET_PATH%
echo [i] Project: _conductor_daemon

:: 3. Запускаем через poetry run
:: Теперь Poetry будет вынужден использовать .venv из своей папки
poetry run python main.py -p "%TARGET_PATH%"

if %ERRORLEVEL% neq 0 (
    echo [!] Daemon stopped with error code %ERRORLEVEL%
    pause
)