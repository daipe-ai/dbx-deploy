import os
from pathlib import Path


def delete_directory_content_recursive(dir_path: Path):
    if dir_path.is_dir():
        file_list = []
        dir_list = []

        for root, dirs, files in os.walk(dir_path):
            for f in files:
                file_list.append(os.path.join(root, f))

            for d in dirs:
                dir_list.append(os.path.join(root, d))

        for f in file_list:
            os.unlink(f)

        for d in dir_list:
            os.rmdir(d)
