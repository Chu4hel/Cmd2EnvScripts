import os
import shutil
import time


class Colors:
    HEADER = '\033[96m'  # Cyan
    OKGREEN = '\033[92m'  # Green
    WARNING = '\033[93m'  # Yellow
    GRAY = '\033[90m'  # Gray
    FAIL = '\033[91m'  # Red
    ENDC = '\033[0m'  # Reset


def print_color(text, color=Colors.ENDC):
    """Выводит цветной текст в консоль."""
    try:
        print(f"{color}{text}{Colors.ENDC}")
    except:
        print(text)


def try_remove_file(path):
    """Безопасное удаление файла (аналог SilentlyContinue)."""
    try:
        os.remove(path)
        return True
    except OSError:
        return False


def try_remove_dir(path):
    """Безопасное удаление папки (аналог SilentlyContinue)."""
    try:
        shutil.rmtree(path, ignore_errors=True)
        return True
    except OSError:
        return False


def cleanup_folder(folder_path, days_old=0):
    """
    Рекурсивно чистит папку.
    :param days_old: Если > 0, удаляет только файлы старше N дней.
                     Если 0, удаляет всё подряд.
    """
    if not os.path.exists(folder_path):
        return 0

    deleted_count = 0
    limit_time = time.time() - (days_old * 86400) if days_old > 0 else None

    # Если days_old=0, эффективнее снести всё через rmtree, но мы хотим оставить саму папку
    # и удалить только содержимое, поэтому используем walk.

    for root, dirs, files in os.walk(folder_path, topdown=False):
        # 1. Удаление файлов
        for name in files:
            file_path = os.path.join(root, name)
            try:
                # Если лимит времени есть - проверяем. Если нет - удаляем сразу.
                if limit_time is None or os.path.getmtime(file_path) < limit_time:
                    os.remove(file_path)
                    deleted_count += 1
            except OSError:
                pass

        # 2. Удаление пустых папок
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                # Удаляем папку, если она пуста.
                # Если включен фильтр по дате, проверяем и дату папки тоже.
                if not os.listdir(dir_path):
                    if limit_time is None or os.path.getmtime(dir_path) < limit_time:
                        os.rmdir(dir_path)
            except OSError:
                pass

    return deleted_count
