import argparse
import os

from ya_disk import y, YA_REMOTE_PATH, YA_LOCAL_PATH
from dotenv import load_dotenv
load_dotenv()

YA_REMOTE_PATH = os.getenv('YA_REMOTE_PATH')


def list_files_and_dirs(y_disk, path, indent=0):
    if y_disk.is_dir(path):
        for item in y_disk.listdir(path):
            item_path = f"{path}/{item['name']}"
            if item['type'] == "dir":
                list_files_and_dirs(y_disk, item_path, indent + 2)
            else:
                print(" " * indent + f"{item_path}")


def download_file(y_disk, remote_path, local_path):
    if y_disk.is_file(remote_path):
        y_disk.download(remote_path, local_path)
        print(f"Файл '{remote_path}' успешно скачан в '{local_path}'.")
    else:
        print(f"Файл '{remote_path}' не найден.")


def main():
    parser = argparse.ArgumentParser(description="Утилита для работы с Яндекс.Диском")

    parser.add_argument(
        '--list',
        action='store_true',
        help="Рекурсивно вывести все папки и файлы с Яндекс.Диска по заданному пути"
    )

    parser.add_argument(
        '--download',
        metavar='REMOTE_FILE',
        type=str,
        help="Скачать файл с Яндекс.Диска по полному названию"
    )

    args = parser.parse_args()

    if not args.list and not args.download:
        parser.error('Требуется хотя бы один из флагов: --list или --download')

    if args.list:
        print(f"Чтение содержимого Яндекс.Диска по пути '{YA_REMOTE_PATH}':")
        list_files_and_dirs(y, YA_REMOTE_PATH)

    if args.download:
        local_path = YA_LOCAL_PATH+'/'+os.path.basename(args.download)
        print(f"Скачивание файла '{args.download}' на локальный диск...")
        download_file(y, args.download, local_path)


if __name__ == "__main__":
    main()
