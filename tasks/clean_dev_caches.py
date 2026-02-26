import argparse
import glob
import os

from _utils import print_color, Colors, cleanup_folder, try_remove_file, try_remove_dir

# Аргументы
parser = argparse.ArgumentParser(description='Clean developer caches.')
parser.add_argument('--days', type=int, default=30, help='Delete files older than N days')
args = parser.parse_args()

USERS_DIR = r"C:\Users"

print_color(f"--- Запуск очистки кэша (старше {args.days} дней) ---", Colors.HEADER)

# Список путей (относительно пользователя)
CACHE_PATHS = [
    # poetry & python
    r"AppData\Local\pypoetry\Cache\artifacts",
    r"AppData\Local\pypoetry\Cache\cache",

    # npm / node
    r"AppData\Local\node-gyp\Cache",
    r"AppData\Local\npm-cache",
    r"AppData\Roaming\npm-cache",

    # Electron Apps (Discord, FACEIT, pgAdmin, SteelSeries, YandexMusic, Postman, etc)
    r"AppData\Roaming\discord\Cache",
    r"AppData\Roaming\discord\Code Cache",
    r"AppData\Roaming\discord\GPUCache",
    r"AppData\Roaming\discord\DawnWebGPUCache",
    r"AppData\Roaming\discord\DawnGraphiteCache",
    r"AppData\Roaming\discord\logs",

    r"AppData\Roaming\FACEIT\Code Cache",
    r"AppData\Roaming\FACEIT\Cache",
    r"AppData\Roaming\FACEIT\GPUCache",
    r"AppData\Roaming\FACEIT\DawnWebGPUCache",
    r"AppData\Roaming\FACEIT\DawnGraphiteCache",

    r"AppData\Roaming\pgadmin4\Code Cache",
    r"AppData\Roaming\pgadmin4\Cache",
    r"AppData\Roaming\pgadmin4\GPUCache",
    r"AppData\Roaming\pgadmin4\DawnWebGPUCache",
    r"AppData\Roaming\pgadmin4\DawnGraphiteCache",

    r"AppData\Roaming\steelseries-gg-client\Cache",
    r"AppData\Roaming\steelseries-gg-client\Code Cache",
    r"AppData\Roaming\steelseries-gg-client\GPUCache",
    r"AppData\Roaming\steelseries-gg-client\DawnWebGPUCache",
    r"AppData\Roaming\steelseries-gg-client\DawnGraphiteCache",

    r"AppData\Roaming\YandexMusic\Cache",
    r"AppData\Roaming\YandexMusic\GPUCache",
    r"AppData\Roaming\YandexMusic\Code Cache",
    r"AppData\Roaming\YandexMusic\logs",
    r"AppData\Roaming\YandexMusic\DawnWebGPUCache",
    r"AppData\Roaming\YandexMusic\DawnGraphiteCache",

    r"AppData\Roaming\Postman\Cache",
    r"AppData\Roaming\Postman\Code Cache",
    r"AppData\Roaming\Postman\logs",

    r"AppData\Roaming\com.adobe.dunamis",

    r"AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\logs",
    r"AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\.crashreport",
]

# Пути, не привязанные к пользователям
SYSTEM_PATHS = [
    r"C:\Windows\LiveKernelReports",  # дампы по 3Гб
    r"C:\$Recycle.Bin",  # Корзина (всех пользователей)
    r"C:\Windows\Temp",  # Системный Temp
]

# Получаем пользователей
try:
    users = os.listdir(USERS_DIR)
except OSError:
    users = []

for user in users:
    user_path = os.path.join(USERS_DIR, user)
    if not os.path.isdir(user_path):
        continue

    # 1. Стандартная очистка путей
    for rel_path in CACHE_PATHS:
        full_path = os.path.join(user_path, rel_path)
        if os.path.exists(full_path):
            print_color(f"Обработка для {user}: {rel_path}", Colors.GRAY)
            count = cleanup_folder(full_path, days_old=args.days)
            if count > 0:
                print_color(f"  -> Очищено файлов: {count}", Colors.OKGREEN)

    # 2. Postman Partitions (UUID папки)
    postman_parts = os.path.join(user_path, r"AppData\Roaming\Postman\Partitions")
    if os.path.exists(postman_parts):
        print_color(f"Очистка Postman Partitions для {user}...", Colors.GRAY)
        try:
            for uuid_folder in os.listdir(postman_parts):
                cache_path = os.path.join(postman_parts, uuid_folder, "Cache")
                cleanup_folder(cache_path, days_old=args.days)
        except OSError:
            pass

    # 3. Яндекс.Диск (удаление старых версий)
    yandex_path = os.path.join(user_path, r"AppData\Roaming\Yandex\YandexDisk2")
    if os.path.exists(yandex_path):
        print_color(f"Анализ Яндекс.Диска для {user}...", Colors.GRAY)
        try:
            versions = [x for x in os.listdir(yandex_path)
                        if os.path.isdir(os.path.join(yandex_path, x)) and x[0].isdigit()]
            versions.sort()

            if len(versions) > 1:
                old_versions = versions[:-1]
                current_version = versions[-1]

                for old in old_versions:
                    print_color(f"  Удаление старой версии: {old}", Colors.WARNING)
                    try_remove_dir(os.path.join(yandex_path, old))

                # Чистим инсталлятор
                current_path = os.path.join(yandex_path, current_version)
                for file in glob.glob(os.path.join(current_path, "*Installer*.exe")):
                    print_color("  Удаление лишнего инсталлятора...", Colors.WARNING)
                    try_remove_file(file)
        except OSError:
            pass

# --- Системная очистка ---
print_color("--- Запуск системной очистки ---", Colors.HEADER)

for sys_path in SYSTEM_PATHS:
    if os.path.exists(sys_path):
        print_color(f"Обработка системного пути: {sys_path}", Colors.GRAY)
        # cleanup_folder применит ваш фильтр --days к файлам внутри
        count = cleanup_folder(sys_path, days_old=args.days)
        if count > 0:
            print_color(f"  -> Удалено объектов: {count}", Colors.OKGREEN)

# Если нужно принудительно очистить корзину полностью (без учета дней),
# можно добавить вызов команды rd /s /q (но лучше придерживаться вашего фильтра по дням)

print_color("--- Готово ---", Colors.HEADER)
