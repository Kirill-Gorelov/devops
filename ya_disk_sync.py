import os

from ya_disk import y, YA_LOCAL_PATH, YA_REMOTE_PATH
from datetime import datetime, timedelta
from telegram import send_message


def clean_and_list_files_and_dirs(y_disk, path, indent=0):
    """
    Удаляет файлы старше 10 дней и пустые папки.
    """
    is_empty = True
    try:
        if y_disk.is_dir(path):
            print(" " * indent + f"Директория: '{path}':")
            for item in y_disk.listdir(path):
                item_path = f"{path}/{item['name']}"
                if item['type'] == "dir":
                    # Рекурсивный вызов для обработки поддиректорий
                    if clean_and_list_files_and_dirs(y_disk, item_path, indent + 2):
                        y_disk.remove(item_path)
                        print(" " * (indent + 2) + f"Пустая директория '{item['name']}' удалена.")
                    else:
                        is_empty = False
                else:
                    file_info = y_disk.get_meta(item_path)
                    modified_time = file_info['modified']

                    # Проверка возраста файла
                    if datetime.now(modified_time.tzinfo) - modified_time > timedelta(days=10):
                        y_disk.remove(item_path)
                        print(" " * (indent + 2) + f"Файл '{item['name']}' удален, так как старше 10 дней.")
                    else:
                        is_empty = False
                        print(" " * (indent + 2) + f"Файл: {item['name']}")

        return is_empty
    except Exception as e:
        send_message('Не удалось синхронизировать файлы бэкапов')


def upload_files(y_disk, local_folder, remote_folder):
    """
    Загружает файлы из локальной папки в указанную директорию на Яндекс.Диске.
    Загружает только те файлы, которых нет на Яндекс.Диске.
    """
    current_date_folder = f"{remote_folder}/{datetime.now().strftime('%Y-%m-%d')}"

    # Создание папки на Яндекс.Диске, если её нет
    if not y_disk.exists(current_date_folder):
        y_disk.mkdir(current_date_folder)
        print(f"Создана новая папка на Яндекс.Диске: '{current_date_folder}'")

    for root, dirs, files in os.walk(local_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = f"{current_date_folder}/{file}"

            # Проверка наличия файла на Яндекс.Диске
            if not y_disk.exists(remote_file_path):
                y_disk.upload(local_file_path, remote_file_path)
                print(f"Файл '{file}' успешно загружен на Яндекс.Диск в '{current_date_folder}'.")
            else:
                print(f"Файл '{file}' уже существует на Яндекс.Диске.")


remote_path = YA_REMOTE_PATH
local_folder = YA_LOCAL_PATH
clean_and_list_files_and_dirs(y, remote_path)
upload_files(y, local_folder, remote_path)
