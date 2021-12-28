import urllib3
from requests.exceptions import HTTPError
from logging import Logger
from databricks_cli.repos.api import ReposApi
from databricks_cli.workspace.api import WorkspaceApi


class RepoManager:
    def __init__(
        self,
        repo_root_dir: str,
        repo_path: str,
        logger: Logger,
        repos_api: ReposApi,
        workspace_api: WorkspaceApi,
    ):
        self.__repos_api = repos_api
        self.__workspace_api = workspace_api
        self.__logger = logger
        self.__repo_root_dir = repo_root_dir
        self.__repo_path = repo_path

    def create_or_update(self, repo_url, branch, tag, repo_name, force):
        repo_path = self.__repo_path.format(repo_name=repo_name)
        self.__logger.info(f"Updating repo at {repo_path}")
        self.__workspace_api.mkdirs(self.__repo_root_dir)

        repo_list = self.__repos_api.list(self.__repo_root_dir, None).get("repos", [])

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
            self.__check_duplicates(repo_list)
            self.__check_correct_project(repo_id, repo_url)
            if force:
                self.__logger.info("Re-cloning repo")
                self.__repos_api.delete(repo_id)
                repo_id = self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]
        except RuntimeError:
            self.__logger.info("Repo not found, cloning new repo")
            self.__check_duplicates(repo_list)
            self.__check_valid_branch(repo_list, branch)
            repo_id = self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]

        try:
            self.__repos_api.update(repo_id=repo_id, branch=branch, tag=tag)
        except HTTPError as e:
            if e.response.json().get("error_code") == "GIT_UNKNOWN_REF":
                self.__logger.info("Error occurred, cleaning up ...")
                self.__repos_api.delete(repo_id)
            raise e

        self.__logger.info("Repo successfully updated")

    def delete(self, repo_url, repo_name):
        repo_path = self.__repo_path.format(repo_name=repo_name)

        self.__logger.info(f"Deleting repo at {repo_path}")

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
            self.__check_correct_project(repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, skipping delete")
        else:
            self.__repos_api.delete(repo_id)
            self.__logger.info("Repo successfully deleted")

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def __check_duplicates(self, repo_list: list):
        repo_branches = [repo.get("branch") for repo in repo_list]
        branch_counter = [{"name": branch, "count": repo_branches.count(branch)} for branch in set(repo_branches)]
        duplicated_branches = [branch["name"] for branch in branch_counter if branch["count"] > 1]
        if len(duplicated_branches) > 0:
            raise Exception(f"Following branches are duplicated in current env: {', '.join(duplicated_branches)}.")

    def __check_valid_branch(self, repo_list: list, branch: str):
        repo_branches = [repo.get("branch") for repo in repo_list]
        if branch in repo_branches:
            raise Exception(f"Branch {branch} is already present in current env.")

    def __get_provider_from_url(self, url):
        provider_map = {
            "github.com": "gitHub",
            "dev.azure.com": "azureDevOpsServices",
        }
        try:
            return provider_map[urllib3.get_host(url)[1]]
        except KeyError:
            raise Exception(f"Git provider for {url} not listed.")
