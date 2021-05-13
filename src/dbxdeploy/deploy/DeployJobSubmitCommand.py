import asyncio
import sys
from logging import Logger
from argparse import Namespace, ArgumentParser
from pathlib import PurePosixPath, Path
from dbxdeploy.deploy.DeployerJobSubmitter import DeployerJobSubmitter
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.notebook.RelativePathResolver import RelativePathResolver
from dbxdeploy.notebook.converter.NotebookConverterInterface import NotebookConverterInterface
from dbxdeploy.notebook.converter.UnexpectedSourceException import UnexpectedSourceException
from dbxdeploy.notebook.loader import load_notebook


class DeployJobSubmitCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        notebook_converter: NotebookConverterInterface,
        deployer_job_submitter: DeployerJobSubmitter,
        relative_path_resolver: RelativePathResolver,
    ):
        self.__logger = logger
        self.__notebook_converter = notebook_converter
        self.__deployer_job_submitter = deployer_job_submitter
        self.__relative_path_resolver = relative_path_resolver

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="notebook_path", help="Databricks notebook path relative to project root")

    def get_command(self) -> str:
        return "dbx:deploy-submit-job"

    def get_description(self):
        return "Deploy to DBX and submit selected notebook as job"

    def run(self, input_args: Namespace):
        relative_notebook_path = PurePosixPath(input_args.notebook_path)
        notebook_path = Path().cwd().joinpath(relative_notebook_path)

        source = load_notebook(notebook_path)

        try:
            self.__notebook_converter.validate_source(source)
        except UnexpectedSourceException:
            self.__logger.error("Only valid Databricks notebooks can be submitted as Databricks job")
            sys.exit(1)

        relative_notebook_path = self.__relative_path_resolver.resolve(relative_notebook_path)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__deployer_job_submitter.deploy_and_submit_job(relative_notebook_path))
