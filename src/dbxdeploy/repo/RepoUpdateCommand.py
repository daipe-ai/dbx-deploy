from argparse import Namespace, ArgumentParser
from logging import Logger
from urllib3 import get_host
from consolebundle.ConsoleCommand import ConsoleCommand
from databricks_cli.repos.api import ReposApi
from databricks_cli.workspace.api import WorkspaceApi
from dbxdeploy.git.CurrentBranchResolver import CurrentBranchResolver


class RepoUpdateCommand(ConsoleCommand):
    def __init__(
        self,
        repos_api: ReposApi,
        workspace_api: WorkspaceApi,
        logger: Logger,
        repo_root_dir: str,
        repo_path: str,
    ):
        self.__repos_api = repos_api
        self.__workspace_api = workspace_api
        self.__logger = logger
        self.__repo_root_dir = "/" + repo_root_dir.strip("/") + "/"
        self.__repo_path = repo_path

    def get_command(self) -> str:
        return "dbx:repo:update"

    def get_description(self):
        return "Pulls and checkouts the current branch of a repo on DBX"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument("--repo-url", dest="repo_url", help="Project repo url")
        argument_parser.add_argument("--checkout-branch", dest="checkout_branch", help="Branch to checkout")
        argument_parser.add_argument("--repo-name", dest="repo_name", help="Project repo name")

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def __check_for_duplicates(self, with_branch: str = None):
        repo_list = self.__repos_api.list(self.__repo_root_dir, None).get("repos", [])
        repo_branches = [repo["branch"] for repo in repo_list]
        if with_branch:
            repo_branches.append(with_branch)
        branch_counter = [{"name": branch, "count": repo_branches.count(branch)} for branch in set(repo_branches)]
        duplicated_branches = [branch["name"] for branch in branch_counter if branch["count"] > 1]

        if len(duplicated_branches) > 0:
            message = f"Following branches are/would be duplicated in current env: {', '.join(duplicated_branches)}."
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
        if not (input_args.repo_url and input_args.checkout_branch and input_args.repo_name):
            raise Exception("All arguments are required. Check -h for the list of arguments.")

        repo_url = input_args.repo_url
        checkout_branch = input_args.checkout_branch
        repo_path = self.__repo_path.format(current_branch=input_args.repo_name)

        self.__workspace_api.mkdirs(self.__repo_root_dir)

        try:
            env_repo_id = self.__repos_api.get_repo_id(repo_path)
            self.__check_for_duplicates()
            self.__check_correct_project(env_repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, cloning new repo")
            self.__check_for_duplicates(with_branch=checkout_branch)
            env_repo_id = self.__repos_api.create(
                url=repo_url,
                provider=self.__get_provider_from_url(repo_url),
                path=repo_path
            )["id"]

        self.__repos_api.update(repo_id=env_repo_id, branch=checkout_branch, tag=None)
        self.__logger.info("Repo successfully pulled")
