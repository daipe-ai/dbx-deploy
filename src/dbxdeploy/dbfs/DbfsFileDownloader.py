from pathlib import Path
from pathlib import PurePosixPath
from typing import List
from base64 import b64decode
from databricks_api import DatabricksAPI
from requests.exceptions import HTTPError


class DbfsFileDownloader:
    def __init__(self, dbx_api: DatabricksAPI):
        self.__dbx_api = dbx_api

    def download(self, dbfs_path: PurePosixPath):
        return self.__streaming_download(dbfs_path)

    def exists(self, dbfs_path: PurePosixPath):
        try:
            self.__dbx_api.dbfs.get_status(dbfs_path)

        except HTTPError as ex:
            if ex.response.status_code != 404:
                raise

            return False

        return True

    def download_directory(self, dbfs_dir: PurePosixPath, local_dir: Path, overwrite: bool = False):
        local_dir.mkdir(exist_ok=True)

        remote_file_paths = self.list_directory_recursive(dbfs_dir, only_files=True)
        local_file_paths = [local_dir.joinpath(file.relative_to(dbfs_dir)) for file in remote_file_paths]

        if not overwrite:
            for local_file_path in local_file_paths:
                if local_dir.joinpath(local_file_path).exists():
                    raise Exception(f"File {local_file_path} already exists")

        for remote_file_path, local_file_path in zip(remote_file_paths, local_file_paths):
            content = self.download(remote_file_path)

            local_file_path.parent.mkdir(parents=True, exist_ok=True)

            with local_file_path.open("wb") as f:
                f.write(content)

    def list_directory_recursive(self, dbfs_dir: PurePosixPath, only_files: bool = False) -> List[PurePosixPath]:
        def recursive_walk(dbfs_dir: PurePosixPath, files: List[PurePosixPath], only_files: bool = False):
            response = self.__dbx_api.dbfs.list(str(dbfs_dir))

            if "files" in response:
                for file in response["files"]:
                    if file["is_dir"]:
                        recursive_walk(file["path"], files, only_files)

                    # always add file
                    if not file["is_dir"]:
                        files.append(PurePosixPath("dbfs:" + file["path"]))

                    # add dir only if only_files=False
                    if file["is_dir"] and not only_files:
                        files.append(PurePosixPath("dbfs:" + file["path"]))

        if not self.exists(dbfs_dir):
            raise Exception(f"Directory at {dbfs_dir} does not exists")

        files = []
        recursive_walk(dbfs_dir, files, only_files)

        return files

    def __streaming_download(self, dbfs_path: PurePosixPath) -> bytes:
        file_info = self.__dbx_api.dbfs.get_status(dbfs_path)

        chunk_size = int(0.5 * 1024 * 1024)  # 0.5MiB
        file_size = file_info["file_size"]
        offset = 0
        data = bytes()

        while offset < file_size:
            response = self.__dbx_api.dbfs.read(dbfs_path, offset, chunk_size)
            offset += response["bytes_read"]
            data += b64decode(response["data"])

        return data
