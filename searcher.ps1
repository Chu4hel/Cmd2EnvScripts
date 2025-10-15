# Этот скрипт принимает один аргумент с командной строки
param (
    [string]$SearchTerm
)

# Проверяем, был ли передан аргумент
if ([string]::IsNullOrEmpty($SearchTerm)) {
    Write-Host ''
    Write-Host '[ Ошибка ] Укажите часть имени команды для поиска.' -ForegroundColor Red
    Write-Host '          Пример: find-cmd devm'
    Write-Host ''
    # Выходим из скрипта
    return
}

# Если аргумент есть, выполняем поиск
Write-Host ''
Write-Host "[ Поиск команд, содержащих '$SearchTerm' ]" -ForegroundColor Yellow
Write-Host '---------------------------------------------------------------------'
Get-Command -Name "*$SearchTerm*" | Select-Object -Property Name, CommandType, Source | Format-Table -AutoSize