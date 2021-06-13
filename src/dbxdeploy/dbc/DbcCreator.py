from logging import Logger
from pathlib import PurePosixPath, Path
from typing import List
import zipfile
from io import BytesIO
from dbxdeploy.dbc.PathsPreparer import PathsPreparer
from dbxdeploy.notebook.Notebook import Notebook
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import load_notebook


class DbcCreator:
    def __init__(
        self,
        working_directory: Path,
        logger: Logger,
        notebook_converter: NotebookConverterInterface,
        paths_preparer: PathsPreparer,
    ):
        self.__working_directory = working_directory
        self.__logger = logger
        self.__notebook_converter = notebook_converter
        self.__paths_preparer = paths_preparer

    def create(self, notebooks: List[Notebook], package_file_path: str, dependencies_dir_path: str) -> bytes:
        databricks_relative_paths = list(map(lambda notebook: notebook.databricks_relative_path, notebooks))
        root_ignored_path_name = "root_ignored_path"

        in_memory_output = BytesIO()

        zip_file = zipfile.ZipFile(in_memory_output, "w", zipfile.ZIP_DEFLATED)

        # directories must be created first, otherwise DataBricks is not able to process that zip/dbc file
        for dir_path in self.__paths_preparer.prepare(databricks_relative_paths, root_ignored_path_name):
            zip_file.writestr(dir_path + "/", "")

        for notebook in notebooks:
            source = load_notebook(notebook.path)

            try:
                self.__notebook_converter.validate_source(source)
            except UnexpectedSourceException:
                self.__logger.debug(f"Skipping unrecognized file {notebook.relative_path}")
                continue

            notebook_source = self.__notebook_converter.to_dbc_notebook(
                notebook.path.stem, source, package_file_path, dependencies_dir_path
            )
            zip_path = PurePosixPath(root_ignored_path_name).joinpath(notebook.databricks_relative_path).with_suffix(".python")
            zip_file.writestr(str(zip_path), notebook_source)

        zip_file.close()
        in_memory_output.seek(0)

        zip_content = in_memory_output.getvalue()
        dist_dir = self.__working_directory.joinpath("dist")

        if not dist_dir.exists():
            dist_dir.mkdir()

        with dist_dir.joinpath("notebooks.dbc").open("wb") as f:
            f.write(zip_content)

        return zip_content
