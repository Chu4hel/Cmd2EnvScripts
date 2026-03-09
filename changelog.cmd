@echo off
setlocal

:: --- НАСТРОЙКИ ---
:: Путь к папке, где лежит ваш main.py и файлы poetry
set SCRIPT_DIR=D:\PROJECTS\ai_commit

:: Точное название модели из LM Studio (как в списке моделей)
set MODEL_NAME=qwen/qwen3-4b-thinking-2507
:: -----------------


:: Переходим в папку скрипта для запуска Poetry
pushd "%SCRIPT_DIR%"

:: Запуск скрипта для чейнджлога
poetry run python shorten_changelog.py --model "%MODEL_NAME%"

:: Возврат в исходную папку
popd

echo.
pause
endlocal
