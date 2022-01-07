import sys
from argparse import Namespace, ArgumentParser
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.repos import argparser_configurator
from dbxdeploy.repos.RepoDeleter import RepoDeleter
from dbxdeploy.repos.RepoPathResolver import RepoPathResolver


class RepoDeleteCommand(ConsoleCommand):
    def __init__(self, logger: Logger, repo_path_resolver: RepoPathResolver, repo_deleter: RepoDeleter):
        self.__logger = logger
        self.__repo_path_resolver = repo_path_resolver
        self.__repo_deleter = repo_deleter

    def get_command(self) -> str:
        return "dbx:repo:delete"

    def get_description(self):
        return "Deletes a repository on DBX if available"

    def configure(self, argument_parser: ArgumentParser):
        argparser_configurator.add_common_repos_args(argument_parser)

    def run(self, input_args: Namespace):
        if not input_args.branch and not input_args.tag:
            self.__logger.error("Either branch or tag must be provided")
            sys.exit(1)

        repo_path = self.__repo_path_resolver.resolve(input_args.repo_name, input_args.branch, input_args.tag)

        self.__repo_deleter.delete(repo_path)
