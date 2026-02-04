import argparse
import glob
import os

from _utils import print_color, Colors, cleanup_folder

# Настройка аргументов
parser = argparse.ArgumentParser(description='Safe cleanup of temporary files.')
parser.add_argument('--days', type=int, default=2, help='Delete files older than N days')
args = parser.parse_args()

# Системные папки
SYSTEM_TEMP = r"C:\Windows\Temp"
USERS_DIR = r"C:\Users"

# Список относительных путей (статические)
RELATIVE_PATHS = [
    r"AppData\Local\Temp",
    r"AppData\Local\CrashDumps",
    r"AppData\Local\Microsoft\Edge\User Data\BrowserMetrics",
    r"AppData\Local\Google\Chrome\User Data\BrowserMetrics",

    # CapCut (еженедельная чистка)
    r"AppData\Local\CapCut\User Data\Cache",
    r"AppData\Local\CapCut\User Data\Log",
    r"AppData\Local\CapCut\User Data\Crash",

    # War Thunder Logs
    r"AppData\Local\WarThunder\.game_logs",
    r"AppData\Local\WarThunder\.launcher_log",

    # DaVinci Resolve Logs (добавил, так как мы договаривались чистить их еженедельно)
    r"AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\logs",
    r"AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\.crashreport"
]


def main():
    print_color(f"--- Запуск безопасной очистки (старше {args.days} дней) ---", Colors.HEADER)

    # Множество для сбора уникальных путей (чтобы не было дублей)
    target_folders = set()

    # 1. Добавляем системный Temp
    if os.path.exists(SYSTEM_TEMP):
        target_folders.add(SYSTEM_TEMP)

    # 2. Собираем папки пользователей
    try:
        users = os.listdir(USERS_DIR)
    except OSError:
        users = []

    for user in users:
        user_path = os.path.join(USERS_DIR, user)
        if not os.path.isdir(user_path):
            continue

        # А. Добавляем статические пути из списка
        for rel_path in RELATIVE_PATHS:
            full_path = os.path.join(user_path, rel_path)
            if os.path.exists(full_path):
                target_folders.add(full_path)

        # Б. Поиск апдейтеров (Appdata\Local\*-updater)
        local_path = os.path.join(user_path, r"AppData\Local")
        if os.path.exists(local_path):
            # glob находит все папки по маске
            for updater in glob.glob(os.path.join(local_path, "*-updater")):
                if os.path.isdir(updater):
                    target_folders.add(updater)

        # В. Поиск логов Photoshop (Appdata\Roaming\Adobe\Adobe Photoshop *\Logs)
        adobe_roaming = os.path.join(user_path, r"AppData\Roaming\Adobe")
        if os.path.exists(adobe_roaming):
            # Ищем папку Logs внутри любой версии фотошопа
            for logs_dir in glob.glob(os.path.join(adobe_roaming, "Adobe Photoshop *", "Logs")):
                if os.path.isdir(logs_dir):
                    target_folders.add(logs_dir)

    # 3. Основной цикл очистки
    print_color(f"Найдено папок для проверки: {len(target_folders)}", Colors.GRAY)

    for folder in target_folders:
        print_color(f"Обработка: {folder}", Colors.GRAY)
        # Вызываем нашу утилиту. Она сама удалит старые файлы и пустые папки.
        count = cleanup_folder(folder, days_old=args.days)

        if count > 0:
            print_color(f"  -> Очищено файлов: {count}", Colors.OKGREEN)

    print_color("--- Готово ---", Colors.HEADER)


if __name__ == "__main__":
    main()
