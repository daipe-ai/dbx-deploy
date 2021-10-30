from argparse import Namespace, ArgumentParser
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from databricks_cli.repos.api import ReposApi


class RepoDeleteCommand(ConsoleCommand):
    def __init__(
        self,
        repos_api: ReposApi,
        logger: Logger,
        repo_root_dir: str,
        repo_path: str,
    ):
        self.__repos_api = repos_api
        self.__logger = logger
        self.__repo_root_dir = "/" + repo_root_dir.strip("/") + "/"
        self.__repo_path = repo_path

    def get_command(self) -> str:
        return "dbx:repo:delete"

    def get_description(self):
        return "Deletes a repository on DBX if available"

    def configure(self, argument_parser: ArgumentParser):
        required_args = argument_parser.add_argument_group('required arguments')
        required_args.add_argument("--repo-url", dest="repo_url", help="Project repo url")
        required_args.add_argument("--repo-name", dest="repo_name", help="Project repo name")

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def run(self, input_args: Namespace):
        if not (input_args.repo_url and input_args.repo_name):
            raise Exception("All arguments are required. Check -h for the list of required arguments.")
        repo_url = input_args.repo_url
        repo_path = self.__repo_path.format(current_branch=input_args.repo_name)

        self.__logger.info(f"Trying to delete repo at {repo_path}")

        try:
            env_repo_id = self.__repos_api.get_repo_id(repo_path)
            self.__check_correct_project(env_repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, skipping delete")
        else:
            self.__repos_api.delete(env_repo_id)
            self.__logger.info("Repo successfully deleted")
