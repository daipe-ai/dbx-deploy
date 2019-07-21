from databricks_api import DatabricksApi
from base64 import b64encode

class Importer:

    def __init__(self, dbx: DatabricksApi):
        self.__dbx = dbx

    def importDbc(self, dbcContent: str, path: str):
        contentToUpload = b64encode(dbcContent).decode()

        self.__dbx.workspace.import_workspace(
            path,
            format='DBC',
            content=contentToUpload
        )
