from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.repos.RepoManager import RepoManager
from dbxdeploy.repos import argparser_configurator


class RepoDeleteCommand(ConsoleCommand):
    def __init__(self, repo_manager: RepoManager):
        self.__repo_manager = repo_manager

    def get_command(self) -> str:
        return "dbx:repo:delete"

    def get_description(self):
        return "Deletes a repository on DBX if available"

    def configure(self, argument_parser: ArgumentParser):
        argparser_configurator.add_common_repos_args(argument_parser)

    def run(self, input_args: Namespace):
        if not input_args.repo_url:
            raise Exception("Missed required arguments. Check -h for the list of required arguments.")

        self.__repo_manager.delete(input_args.repo_url, input_args.repo_name, input_args.branch, input_args.tag)
