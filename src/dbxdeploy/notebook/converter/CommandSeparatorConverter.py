import re
from dbxdeploy.dbc.CommandsConverter import CommandsConverter
from dbxdeploy.notebook.converter import empty_lines_remover
from dbxdeploy.notebook.converter.CellsExtractor import CellsExtractor
from dbxdeploy.notebook.converter.DbcScriptRenderer import DbcScriptRenderer
from dbxdeploy.notebook.converter.JinjaTemplateLoader import JinjaTemplateLoader
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.package.PackageInstaller import PackageInstaller
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface


class CommandSeparatorConverter(NotebookConverterInterface):

    first_line = "# Databricks notebook source"
    cell_separator = "# COMMAND ----------"

    def __init__(
        self,
        commands_converter: CommandsConverter,
        cells_extractor: CellsExtractor,
        jinja_template_loader: JinjaTemplateLoader,
        dbc_script_renderer: DbcScriptRenderer,
        package_installer: PackageInstaller,
    ):
        self.__commands_converter = commands_converter
        self.__cells_extractor = cells_extractor
        self.__jinja_template_loader = jinja_template_loader
        self.__dbc_script_renderer = dbc_script_renderer
        self.__package_installer = package_installer

    def validate_source(self, source: str):
        if re.match(r"^" + self.first_line + "[\r\n]", source) is None:
            raise UnexpectedSourceException()

    def from_dbc_notebook(self, content: dict) -> str:
        return self.__commands_converter.convert(content["commands"], self.first_line, self.cell_separator)

    def to_dbc_notebook(self, notebook_name: str, source: str, package_file_path: str, dependencies_dir_path: str) -> str:
        cells = self.__cells_extractor.extract(source, r"#[\s]+COMMAND[\s]+[\-]+\n+")

        def cleanup_cell(cell: dict):
            if cell["source"] == "# MAGIC %install_master_package_whl":
                cell["source"] = self.__package_installer.get_package_install_command(package_file_path, dependencies_dir_path)

            cell["source"] = re.sub(r"^" + self.first_line + "[\r\n]+", "", cell["source"])
            cell["source"] = re.sub(r"# MAGIC\s*", "", cell["source"])
            cell["source"] = empty_lines_remover.remove(cell["source"])

            return cell

        cells = list(map(cleanup_cell, cells))

        template = self.__jinja_template_loader.load()

        return self.__dbc_script_renderer.render(notebook_name, template, cells)

    def to_workspace_import_notebook(self, source: str, package_file_path: str, dependencies_dir_path: str) -> str:
        source = empty_lines_remover.remove(source)
        source = source.replace(
            "# MAGIC %install_master_package_whl",
            self.__package_installer.get_package_install_command(package_file_path, dependencies_dir_path),
        )

        return source
