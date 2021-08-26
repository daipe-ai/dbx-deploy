from urllib.parse import urlparse
from dbxdeploy.package.PackageIndexResolver import PackageIndexResolver


class PackageInstaller:
    def __init__(
        self,
        package_base_dir: str,
        offline_install: bool,
        package_index_resolver: PackageIndexResolver,
    ):
        self.__package_base_dir = package_base_dir
        self.__offline_install = offline_install
        self.__package_index_resolver = package_index_resolver

    def get_package_install_command(self, package_file_path: str, dependencies_dir_path: str):
        if self.__offline_install:
            return self.__get_offline_install_command(package_file_path, dependencies_dir_path)

        return self.__get_online_install_command(package_file_path)

    def is_package_install_command(self, command_code: str):
        return command_code.startswith("# %install_master_package_whl")

    def __modify_dbfs(self, path: str):
        return "/dbfs/" + path.lstrip("dbfs:/")

    def __get_install_command(self, package_file_path: str, options: [str]):
        pip_options = " ".join(options)

        return (
            "# %install_master_package_whl\n"
            "import IPython\n"
            "import os\n"
            "ipy = IPython.get_ipython()\n"
            "ipy.run_line_magic"
            f"('pip', 'install {self.__modify_dbfs(package_file_path)} {pip_options}') # noqa E501"
        )

    def __get_online_install_command(self, package_file_path: str):
        options = []

        if self.__package_index_resolver.has_default_index():
            options.append(f"{self.__get_index_url_part()}")

        if self.__package_index_resolver.has_secondary_indexes():
            options.append(f"{self.__get_extra_index_url_part()}")

        install_command = self.__get_install_command(package_file_path, options)

        return install_command

    def __get_offline_install_command(self, package_file_path: str, dependencies_dir_path: str):
        options = ["--no-index", f"--find-links {self.__modify_dbfs(dependencies_dir_path)}"]
        install_command = self.__get_install_command(package_file_path, options)

        return install_command

    def __get_index_url_part(self):
        default_index = self.__package_index_resolver.get_default_index()
        default_index_url = default_index["url"]
        username_env_var_name = f'DATABRICKS_HTTP_BASIC_{default_index["name"]}_USERNAME'.upper()
        password_env_var_name = f'DATABRICKS_HTTP_BASIC_{default_index["name"]}_PASSWORD'.upper()

        parsed_url = urlparse(default_index_url)

        if "@" not in parsed_url.netloc:
            parsed_url = parsed_url._replace(
                netloc=f'{{os.getenv("{username_env_var_name}")}}:{{os.getenv("{password_env_var_name}")}}@{parsed_url.netloc}'
            )

        return f"--index-url {parsed_url.geturl()}"

    def __get_extra_index_url_part(self):
        extra_indexes = self.__package_index_resolver.get_secondary_indexes()
        extra_indexes_to_return = []

        for extra_index in extra_indexes:
            extra_index_url = extra_index["url"]
            username_env_var_name = f'DATABRICKS_HTTP_BASIC_{extra_index["name"]}_USERNAME'.upper()
            password_env_var_name = f'DATABRICKS_HTTP_BASIC_{extra_index["name"]}_PASSWORD'.upper()

            parsed_url = urlparse(extra_index_url)

            if "@" not in parsed_url.netloc:
                parsed_url = parsed_url._replace(
                    netloc=f'{{os.getenv("{username_env_var_name}")}}:{{os.getenv("{password_env_var_name}")}}@{parsed_url.netloc}'
                )

            extra_indexes_to_return.append(f"--extra-index-url {parsed_url.geturl()}")

        return " ".join(extra_indexes_to_return)
