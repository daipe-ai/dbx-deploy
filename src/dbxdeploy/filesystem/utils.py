import os
from pathlib import Path


def delete_directory_content_recursive(dir_path: Path):
    if dir_path.is_dir():
        file_list = []
        dir_list = []

        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_list.append(os.path.join(root, file))

            for dir_ in dirs:
                dir_list.append(os.path.join(root, dir_))

        for file in file_list:
            os.unlink(file)

        for dir_ in dir_list:
            os.rmdir(dir_)
