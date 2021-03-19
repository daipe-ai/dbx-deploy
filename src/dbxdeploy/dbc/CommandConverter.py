import re
from dbxdeploy.package.PackageInstaller import PackageInstaller


class CommandConverter:
    def __init__(
        self,
        package_installer: PackageInstaller,
    ):
        self.__package_installer = package_installer

    def convert(self, command: dict):
        if self.__package_installer.is_package_install_command(command["command"]):
            return self.__process_title("# MAGIC %install_master_package_whl", command)

        magic_command = self.__detect_magic_command(command["command"])

        if magic_command:
            command_code = "# MAGIC " + command["command"].replace("\n", "\n# MAGIC ")

            return self.__process_title(command_code, command)

        return self.__process_title(command["command"], command)

    def __detect_magic_command(self, command_code: str):
        matches = re.match(r"^(%[a-z_]+)[\s]", command_code)

        if not matches:
            return None

        return matches.group(1)

    def __process_title(self, command_code: str, orig_command: dict):
        if not orig_command["commandTitle"]:
            return command_code

        show_command_title_string = "1" if orig_command["showCommandTitle"] is True else "0"

        return f'# DBTITLE {show_command_title_string},{orig_command["commandTitle"]}\n{command_code}'
