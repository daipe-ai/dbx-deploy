from io import BytesIO
import zipfile


class DbcFilesHandler:
    def handle(self, dbc_content: bytes, callback: callable):
        buffer = BytesIO()
        buffer.write(dbc_content)

        zip_file = zipfile.ZipFile(buffer, "r", zipfile.ZIP_DEFLATED)

        for file in zip_file.filelist:
            callback(zip_file, file)

        zip_file.close()
        buffer.seek(0)
