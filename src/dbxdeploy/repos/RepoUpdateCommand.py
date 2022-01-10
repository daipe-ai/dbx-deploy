import sys
from argparse import Namespace, ArgumentParser
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from dbxdeploy.repos.RepoCreator import RepoCreator
from dbxdeploy.repos.RepoUpdater import RepoUpdater
from dbxdeploy.repos import argparser_configurator
from dbxdeploy.repos.RepoPathResolver import RepoPathResolver


class RepoUpdateCommand(ConsoleCommand):
    def __init__(self, logger: Logger, repo_path_resolver: RepoPathResolver, repo_creator: RepoCreator, repo_updater: RepoUpdater):
        self.__logger = logger
        self.__repo_path_resolver = repo_path_resolver
        self.__repo_creator = repo_creator
        self.__repo_updater = repo_updater

    def get_command(self) -> str:
        return "dbx:repo:update"

    def get_description(self):
        return "Pulls and checkouts the current branch of a repo on DBX"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--repo-url", dest="repo_url", help="Project repo url")
        argparser_configurator.add_common_repos_args(argument_parser)
        argument_parser.add_argument("--force", "-f", dest="force", action="store_true", help="Force update")
        argument_parser.set_defaults(force=False)

    def run(self, input_args: Namespace):
        if not input_args.repo_url:
            self.__logger.error("Missed required arguments. Check -h for the list of required arguments.")
            sys.exit(1)

        if not input_args.branch and not input_args.tag:
            self.__logger.error("Either branch or tag must be provided")
            sys.exit(1)

        if input_args.branch and input_args.tag:
            self.__logger.error("Both branch and tag cannot be provided")
            sys.exit(1)

        repo_path = self.__repo_path_resolver.resolve(input_args.repo_name, input_args.branch, input_args.tag)

        if input_args.force:
            repo_id = self.__repo_creator.recreate(input_args.repo_url, repo_path)
        else:
            repo_id = self.__repo_creator.find_or_create(input_args.repo_url, repo_path)

        if input_args.branch:
            self.__repo_updater.create_or_update_branch(repo_id, input_args.branch)
            self.__logger.info(f"Repo {repo_path} successfully updated to branch {input_args.branch}")

        if input_args.tag:
            self.__repo_updater.create_or_update_tag(repo_id, input_args.tag)
            self.__logger.info(f"Repo {repo_path} successfully updated to tag {input_args.tag}")
