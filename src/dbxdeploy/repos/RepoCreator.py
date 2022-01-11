import os
import urllib3
from logging import Logger
from databricks_cli.repos.api import ReposApi
from databricks_cli.workspace.api import WorkspaceApi


class RepoCreator:
    def __init__(
        self,
        logger: Logger,
        repos_api: ReposApi,
        workspace_api: WorkspaceApi,
    ):
        self.__logger = logger
        self.__repos_api = repos_api
        self.__workspace_api = workspace_api

    def find_or_create(self, repo_url: str, repo_path: str) -> int:
        repo_group_path = os.path.split(repo_path)[0]
        self.__logger.info(f"Updating repo at {repo_path}")
        self.__workspace_api.mkdirs(repo_group_path)

        repo_list = self.__repos_api.list(repo_group_path, None).get("repos", [])
        self.__check_duplicated_branches(repo_list)

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
        except RuntimeError:
            self.__logger.info(f"Repo {repo_path} not found, cloning new repo from {repo_url}")
            return self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]

        self.__check_correct_project(repo_id, repo_url)

        return repo_id

    def recreate(self, repo_url: str, repo_path: str):
        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
        except RuntimeError as e:
            if "Can't find repo ID" in str(e):
                repo_group_path = os.path.split(repo_path)[0]
                self.__workspace_api.mkdirs(repo_group_path)
            else:
                raise e
        else:
            self.__logger.info(f"Deleting repo {repo_path}")
            self.__repos_api.delete(repo_id)

        self.__logger.info(f"Creating repo {repo_path} from {repo_url}")
        return self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def __check_duplicated_branches(self, repo_list: list):
        repo_branches = [repo.get("branch") for repo in repo_list]
        branch_counter = [{"name": branch, "count": repo_branches.count(branch)} for branch in set(repo_branches)]
        duplicated_branches = [branch["name"] for branch in branch_counter if branch["count"] > 1]
        if len(duplicated_branches) > 0:
            raise Exception(f"Following branches are duplicated in current env: {', '.join(duplicated_branches)}.")

    def __get_provider_from_url(self, url):
        provider_map = {
            "github.com": "gitHub",
            "dev.azure.com": "azureDevOpsServices",
        }
        try:
            return provider_map[urllib3.get_host(url)[1]]
        except KeyError as e:
            raise Exception(f"Git provider for {url} not listed.") from e
