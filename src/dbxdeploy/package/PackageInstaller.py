import re


class PackageInstaller:
    def __init__(
        self,
        package_base_dir: str,
        offline_install: bool,
    ):
        self.__package_base_dir = package_base_dir
        self.__offline_install = offline_install

    def get_package_install_command(self, package_file_path: str, dependencies_dir_path: str):
        if self.__offline_install:
            return self.__get_offline_install_command(package_file_path, dependencies_dir_path)

        return self.__get_online_install_command(package_file_path)

    def is_package_install_command(self, command_code: str):
        reg_exp = "^" + re.escape(f"%pip install {self.__modify_dbfs(self.__package_base_dir)}") + ".+-py3-none-any.whl"

        return re.match(reg_exp, command_code) is not None

    def __modify_dbfs(self, path: str):
        return "/dbfs/" + path.lstrip("dbfs:/")

    def __get_online_install_command(self, package_file_path: str):
        return f"%pip install {self.__modify_dbfs(package_file_path)}"

    def __get_offline_install_command(self, package_file_path: str, dependencies_dir_path: str):
        return f"%pip install {self.__modify_dbfs(package_file_path)} --no-index --find-links {self.__modify_dbfs(dependencies_dir_path)}"
