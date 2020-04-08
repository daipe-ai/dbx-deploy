import re

class CommandConverter:

    def __init__(
        self,
        whlBaseDir: str,
    ):
        self.__whlBaseDir = whlBaseDir

    def convert(self, command: dict):
        if command['command'][0:5] == '%run ' or command['command'][0:4] == '%md ':
            return '# MAGIC ' + command['command']

        if command['commandTitle']:
            return '# DBTITLE 1,' + command['commandTitle'] + '\n' + command['command']

        regExp = (
            '^' + re.escape('dbutils.library.install(\'' + self.__whlBaseDir) +
            '/[^/]+/[\\d]{4}-[\\d]{2}-[\\d]{2}_[\\d]{2}-[\\d]{2}-[\\d]{2}_[\\w]+/[^-]+-[\\d.]+-py3-none-any.whl\'\\)$'
        )

        if re.match(regExp, command['command']):
            return '# MAGIC %installMasterPackageWhl'

        return command['command']
