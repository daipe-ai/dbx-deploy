from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.repos.RepoManager import RepoManager


class RepoDeleteCommand(ConsoleCommand):
    def __init__(self, repo_manager: RepoManager):
        self.__repo_manager = repo_manager

    def get_command(self) -> str:
        return "dbx:repo:delete"

    def get_description(self):
        return "Deletes a repository on DBX if available"

    def configure(self, argument_parser: ArgumentParser):
        required_args = argument_parser.add_argument_group("required arguments")
        required_args.add_argument("--repo-url", dest="repo_url", help="Project repo url")
        required_args.add_argument("--repo-name", dest="repo_name", help="Project repo name")

    def run(self, input_args: Namespace):
        if not (input_args.repo_url and input_args.repo_name):
            raise Exception("All arguments are required. Check -h for the list of required arguments.")

        self.__repo_manager.delete(input_args.repo_url, input_args.repo_name)
