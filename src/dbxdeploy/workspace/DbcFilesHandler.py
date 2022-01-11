from typing import Callable

from io import BytesIO
import zipfile


class DbcFilesHandler:
    def handle(self, dbc_content: bytes, callback: Callable):
        buffer = BytesIO()
        buffer.write(dbc_content)

        with zipfile.ZipFile(buffer, "r", zipfile.ZIP_DEFLATED) as zip_file:
            for file in zip_file.filelist:
                callback(zip_file, file)

        buffer.seek(0)
