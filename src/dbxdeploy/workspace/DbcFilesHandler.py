from io import BytesIO
import zipfile

class DbcFilesHandler:

    def handle(self, dbcContent: bytes, callback: callable):
        buffer = BytesIO()
        buffer.write(dbcContent)

        zipFile = zipfile.ZipFile(buffer, 'r', zipfile.ZIP_DEFLATED)

        for file in zipFile.filelist:
            callback(zipFile, file)

        zipFile.close()
        buffer.seek(0)
