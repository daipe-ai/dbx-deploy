from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.repos.RepoManager import RepoManager
from dbxdeploy.repos import argparser_configurator


class RepoUpdateCommand(ConsoleCommand):
    def __init__(self, repo_manager: RepoManager):
        self.__repo_manager = repo_manager

    def get_command(self) -> str:
        return "dbx:repo:update"

    def get_description(self):
        return "Pulls and checkouts the current branch of a repo on DBX"

    def configure(self, argument_parser: ArgumentParser):
        argparser_configurator.add_common_repos_args(argument_parser)
        argument_parser.add_argument("--force", "-f", dest="force", action="store_true", help="Force update")
        argument_parser.set_defaults(force=False)

    def run(self, input_args: Namespace):
        if not input_args.repo_url:
            raise Exception("Missed required arguments. Check -h for the list of required arguments.")

        self.__repo_manager.create_or_update(
            input_args.repo_url,
            input_args.repo_name,
            input_args.branch,
            input_args.tag,
            input_args.force,
        )
