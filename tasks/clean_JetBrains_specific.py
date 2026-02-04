import argparse
import os

from _utils import print_color, Colors, cleanup_folder

# --- Настройка аргументов ---
parser = argparse.ArgumentParser(
    description='Универсальный скрипт для очистки JetBrains.',
    formatter_class=argparse.RawTextHelpFormatter  # Для красивого вывода help
)
parser.add_argument(
    '--user',
    required=True,
    help='Имя пользователя Windows (например, SergoWork).'
)

# Группа взаимоисключающих режимов
mode_group = parser.add_mutually_exclusive_group()
mode_group.add_argument(
    '--full-clean',
    action='store_true',
    help='Режим полной очистки: удаляет ВСЕ кэши, индексы и логи.'
)
mode_group.add_argument(
    '--days-heavy-cache',
    type=int,
    default=180,
    help='Режим умной очистки: удаляет тяжелые кэши старше N дней (по умолчанию: 180).'
)

args = parser.parse_args()

# --- Основная логика ---
BASE_PATH = rf"C:\Users\{args.user}\AppData\Local\JetBrains"


def main():
    print_color(f"--- Запуск очистки JetBrains для пользователя: {args.user} ---", Colors.HEADER)

    if not os.path.exists(BASE_PATH):
        print_color(f"Папка не найдена: {BASE_PATH}", Colors.WARNING)
        return

    # --- Определяем, что и как чистить, в зависимости от режима ---

    # 1. Легкий мусор: логи, tmp, отчеты о вылетах
    light_targets = ['log', 'tmp', 'crash-reports']

    # 2. Тяжелый мусор: кэши, индексы, дистрибутивы
    heavy_targets = [
        'caches', 'index', 'imagecache', 'jcef_cache',
        'jetbrainsclientdist', 'cpython-cache', 'vcs-log'
    ]

    if args.full_clean:
        # РЕЖИМ 1: ПОЛНАЯ ОЧИСТКА
        print_color("!!! РЕЖИМ ПОЛНОЙ ОЧИСТКИ !!!", Colors.WARNING)
        all_targets = light_targets + heavy_targets

        for root, dirs, files in os.walk(BASE_PATH):
            for dirname in dirs:
                if dirname.lower() in all_targets:
                    full_path = os.path.join(root, dirname)
                    print_color(f"  Очистка: {full_path}", Colors.GRAY)
                    # days_old=0 означает "удалить всё"
                    cleanup_folder(full_path, days_old=0)
    else:
        # РЕЖИМ 2: УМНАЯ ОЧИСТКА (по умолчанию)
        print_color(f"РЕЖИМ УМНОЙ ОЧИСТКИ (тяжелый кэш старше {args.days_heavy_cache} дней)", Colors.HEADER)

        # а) Чистим легкий мусор старше 2 дней
        print_color("\n[1] Очистка логов и временных файлов...", Colors.CYAN)
        for root, dirs, files in os.walk(BASE_PATH):
            for dirname in dirs:
                if dirname.lower() in light_targets:
                    full_path = os.path.join(root, dirname)
                    count = cleanup_folder(full_path, days_old=2)
                    if count > 0:
                        print_color(f"  Очищено файлов в {dirname}: {count}", Colors.OKGREEN)

        # б) Чистим тяжелый мусор старше N дней
        print_color(f"\n[2] Очистка тяжелого кэша...", Colors.CYAN)
        for root, dirs, files in os.walk(BASE_PATH):
            for dirname in dirs:
                if dirname.lower() in heavy_targets:
                    full_path = os.path.join(root, dirname)
                    count = cleanup_folder(full_path, days_old=args.days_heavy_cache)
                    if count > 0:
                        print_color(f"  Очищено старых файлов в {dirname}: {count}", Colors.OKGREEN)

    print_color("\n--- Готово ---", Colors.HEADER)


if __name__ == "__main__":
    main()
