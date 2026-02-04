@echo off
setlocal

:: --- НАСТРОЙКИ ---
:: Путь к папке, где лежит ваш main.py и файлы poetry
set SCRIPT_DIR=D:\PROJECTS\ai_commit

:: Точное название модели из LM Studio (как в списке моделей)
set MODEL_NAME=qwen/qwen3-4b-thinking-2507
:: -----------------

:: Сохраняем путь к текущему проекту, где мы вызвали команду
set TARGET_DIR=%CD%

:: Переходим в папку скрипта для запуска Poetry
pushd "%SCRIPT_DIR%"

:: Запуск
poetry run python main.py --model "%MODEL_NAME%" --cwd "%TARGET_DIR%" --clipboard

:: Возврат в исходную папку
popd

endlocal