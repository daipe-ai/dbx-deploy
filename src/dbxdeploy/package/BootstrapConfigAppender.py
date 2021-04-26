import json
import zipfile
from pyfonycore import pyproject
from pyfonycore.bootstrap.config.raw import raw_config_reader
from pathlib import Path


class BootstrapConfigAppender:
    def append(self, package_path: Path):
        package_file_name = package_path.stem
        package_file_name_parts = package_file_name.split("-")
        package_name = package_file_name_parts[0].replace("__", "_")  # __myproject__ needs to be converted to _myproject_ for some reason

        dist_info_dir = f"{package_name}-{package_file_name_parts[1]}.dist-info"

        zip_file = zipfile.ZipFile(package_path, "a")
        zip_file.writestr(dist_info_dir + "/entry_points.txt", self.__prepare_entry_points(package_name))
        zip_file.writestr(dist_info_dir + "/bootstrap_config.json", self.__prepare_bootstrap_config())
        zip_file.close()

    def __prepare_entry_points(self, package_name):
        return f"[pyfony.bootstrap]\npackage_name={package_name}\n"

    def __prepare_bootstrap_config(self):
        bootstrap_config = raw_config_reader.read(pyproject.get_path())
        return json.dumps(bootstrap_config)
