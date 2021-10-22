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
        self.__branch = current_branch_resolver.resolve()
        self.__logger = logger
        self.__repo_root_dir = "/" + repo_root_dir.strip("/") + "/"
        self.__repo_path = repo_path.format(repo_name=self.__branch)

    def get_command(self) -> str:
        return "dbx:repo:pull"

    def get_description(self):
        return "Pulls a latest version of a repository on DBX"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--repo-url", dest="repo_url", help="Project repo url")

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def __check_for_duplicates(self, repo_to_be_created: bool):
        repo_list = self.__repos_api.list(self.__repo_root_dir, None)["repos"]
        repo_branches = [repo["branch"] for repo in repo_list]
        if repo_to_be_created:
            repo_branches.append(self.__branch)
        branch_counter = [{"name": branch, "count": repo_branches.count(branch)} for branch in set(repo_branches)]
        duplicated_branches = [branch["name"] for branch in branch_counter if branch["count"] > 1]

        if len(duplicated_branches) > 0:
            message = f"Following branches are duplicated in current env: {', '.join(duplicated_branches)}."
            if repo_to_be_created:
                message = f"Can't create repo. Following branches would be duplicated in current env: {', '.join(duplicated_branches)}."
            raise Exception(message)

    @staticmethod
    def __get_provider_from_url(url):
        provider_map = {
            "github.com": "gitHub",
            "dev.azure.com": "azureDevOpsServices",
        }
        try:
            return provider_map[get_host(url)[1]]
        except KeyError:
            raise Exception(f"Git provider for {url} not listed.")

    def run(self, input_args: Namespace):
        repo_url = input_args.repo_url

        self.__logger.info(f"Branch: {self.__branch}")

        self.__workspace_api.mkdirs(self.__repo_root_dir)

        try:
            env_repo_id = self.__repos_api.get_repo_id(self.__repo_path)
            self.__check_for_duplicates(repo_to_be_created=False)
            self.__check_correct_project(env_repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, cloning new repo")
            self.__check_for_duplicates(repo_to_be_created=True)
            env_repo_id = self.__repos_api.create(
                url=repo_url,
                provider=self.__get_provider_from_url(repo_url),
                path=self.__repo_path
            )["id"]
        self.__repos_api.update(repo_id=env_repo_id, branch=self.__branch, tag=None)
        self.__logger.info("Repo successfully pulled")
