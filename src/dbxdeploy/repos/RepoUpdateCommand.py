from argparse import Namespace, ArgumentParser
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.repos.RepoManager import RepoManager


class RepoUpdateCommand(ConsoleCommand):
    def __init__(self, repo_manager: RepoManager):
        self.__repo_manager = repo_manager

    def get_command(self) -> str:
        return "dbx:repo:update"

    def get_description(self):
        return "Pulls and checkouts the current branch of a repo on DBX"

    def configure(self, argument_parser: ArgumentParser):
        required_args = argument_parser.add_argument_group("required arguments")
        required_choice_args = argument_parser.add_argument_group("required one of these")
        optional_args = argument_parser.add_argument_group("optional arguments")
        required_args.add_argument("--repo-url", dest="repo_url", help="Project repo url")
        required_args.add_argument("--repo-name", dest="repo_name", help="Project repo name")
        required_choice_args.add_argument("--branch", dest="branch", help="Branch to checkout")
        required_choice_args.add_argument("--tag", dest="tag", help="Tag to checkout")
        optional_args.add_argument("--force", "-f", dest="force", action="store_true", help="Force update")
        optional_args.set_defaults(force=False)

    def run(self, input_args: Namespace):
        if not (input_args.repo_url and input_args.repo_name) or not (input_args.branch or input_args.tag):
            raise Exception("Missed required arguments. Check -h for the list of required arguments.")
        if input_args.branch and input_args.tag:
            raise Exception("Can't pick both --checkout-branch and --checkout-tag. Check -h for details.")

        self.__repo_manager.create_or_update(
            input_args.repo_url,
            input_args.branch,
            input_args.tag,
            input_args.repo_name,
            input_args.force,
        )
