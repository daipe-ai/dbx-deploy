from argparse import Namespace, ArgumentParser
from logging import Logger
from consolebundle.ConsoleCommand import ConsoleCommand
from databricks_cli.repos.api import ReposApi
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver


class RepoDeleteCommand(ConsoleCommand):
    def __init__(
        self,
        repos_api: ReposApi,
        current_branch_resolver: CurrentBranchResolver,
        logger: Logger,
        repo_root_dir: str,
        repo_path: str,
    ):
        self.__repos_api = repos_api
        self.__branch = current_branch_resolver.resolve()
        self.__logger = logger
        self.__repo_root_dir = "/" + repo_root_dir.strip("/") + "/"
        self.__repo_path = repo_path.format(repo_name=self.__branch)

    def get_command(self) -> str:
        return "dbx:repo:delete"

    def get_description(self):
        return "Deletes a repository on DBX if available"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--repo-url", dest="repo_url", help="Project repo url")

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def run(self, input_args: Namespace):
        repo_url = input_args.repo_url
        self.__repo_path = self.__repo_path.format(repo_name=self.__branch)

        self.__logger.info(f"Branch: {self.__branch}")

        try:
            env_repo_id = self.__repos_api.get_repo_id(self.__repo_path)
            self.__check_correct_project(env_repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, skipping delete")
        else:
            self.__repos_api.delete(env_repo_id)
            self.__logger.info("Repo successfully deleted")
