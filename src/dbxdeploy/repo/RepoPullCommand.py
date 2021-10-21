from argparse import Namespace, ArgumentParser
from logging import Logger
from urllib3 import get_host
from consolebundle.ConsoleCommand import ConsoleCommand
from databricks_cli.repos.api import ReposApi
from databricks_cli.workspace.api import WorkspaceApi
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver


class RepoPullCommand(ConsoleCommand):
    def __init__(
        self,
        repos_api: ReposApi,
        workspace_api: WorkspaceApi,
        current_branch_resolver: CurrentBranchResolver,
        logger: Logger,
        repo_root_dir: str,
        repo_path: str,
    ):
        self.__repos_api = repos_api
        self.__workspace_api = workspace_api
        self.__current_branch_resolver = current_branch_resolver
        self.__logger = logger
        self.__repo_root_dir = "/" + repo_root_dir.strip("/") + "/"
        self.__repo_path = repo_path

    def get_command(self) -> str:
        return "dbx:repo:pull"

    def get_description(self):
        return "Pulls a latest version of a repository on DBX"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--repo-url", dest="repo_url", help="Project repo url")

    def _check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    @staticmethod
    def _get_provider_from_url(url):
        provider_map = {
            "github.com": "gitHub",
            "dev.azure.com": "azureDevOpsServices",
        }
        try:
            return provider_map[get_host(url)[1]]
        except KeyError:
            raise Exception(f"Git provider for {url} not listed.")

    def run(self, input_args: Namespace):
        branch = self.__current_branch_resolver.resolve()
        repo_url = input_args.repo_url
        self.__repo_path = self.__repo_path.format(repo_name=branch)

        self.__logger.info(f"Branch: {branch}")

        self.__workspace_api.mkdirs(self.__repo_root_dir)

        try:
            env_repo_id = self.__repos_api.get_repo_id(self.__repo_path)
            self._check_correct_project(env_repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, cloning new repo")
            env_repo_id = self.__repos_api.create(
                url=repo_url,
                provider=self._get_provider_from_url(repo_url),
                path=self.__repo_path
            )["id"]
        self.__repos_api.update(repo_id=env_repo_id, branch=branch, tag=None)
        self.__logger.info("Repo successfully pulled")
