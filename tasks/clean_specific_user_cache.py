import argparse
import os

from _utils import print_color, Colors, cleanup_folder

# Настройка аргументов
parser = argparse.ArgumentParser(description='Clean specific caches for a specific user.')
parser.add_argument('--user', required=True, help='Windows username (e.g. TechAdmin)')
args = parser.parse_args()

# Базовый путь к профилю
USER_PATH = os.path.join(r"C:\Users", args.user)

# Список относительных путей для очистки
# Здесь мы перечисляем то, что нужно чистить "под ноль" для этого пользователя
TARGET_FOLDERS = [
    r"AppData\Local\NVIDIA\DXCache",
    r"AppData\Local\NVIDIA\GLCache"
]


def main():
    print_color(f"--- Запуск точечной очистки для пользователя: {args.user} ---", Colors.HEADER)

    if not os.path.exists(USER_PATH):
        print_color(f"Пользователь не найден: {args.user}", Colors.FAIL)
        return

    for rel_path in TARGET_FOLDERS:
        full_path = os.path.join(USER_PATH, rel_path)

        if os.path.exists(full_path):
            print_color(f"Очистка: {full_path}", Colors.GRAY)
            # days_old=0 означает "удалить всё, независимо от даты"
            # (аналог Remove-Item -Force без фильтра по дате)
            count = cleanup_folder(full_path, days_old=0)
            if count > 0:
                print_color(f"  -> Удалено файлов: {count}", Colors.OKGREEN)
        else:
            # Можно раскомментировать, если хотите знать, что папки нет
            # print_color(f"Папка не найдена (пропуск): {rel_path}", Colors.GRAY)
            pass

    print_color("--- Готово ---", Colors.HEADER)


if __name__ == "__main__":
    main()
