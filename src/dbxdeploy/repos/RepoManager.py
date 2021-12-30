import os
import urllib3
from logging import Logger
from requests.exceptions import HTTPError
from databricks_cli.repos.api import ReposApi
from databricks_cli.workspace.api import WorkspaceApi


class RepoManager:
    def __init__(
        self,
        repo_root_dir: str,
        repo_path: str,
        repo_base_dir: str,
        logger: Logger,
        repos_api: ReposApi,
        workspace_api: WorkspaceApi,
    ):
        if repo_root_dir is not None or repo_path is not None:
            raise Exception(
                "dbxdeploy.target.repo.root_dir and dbxdeploy.target.repo.path are deprecated, please use dbxdeploy.target.repo.base_dir instead"
            )

        self.__repo_base_dir = repo_base_dir
        self.__logger = logger
        self.__repos_api = repos_api
        self.__workspace_api = workspace_api

    def create_or_update(self, repo_url, repo_name=None, branch=None, tag=None, force=False):
        repo_path = self.__resolve_repo_path(repo_name, branch, tag)
        repo_group_path = os.path.split(repo_path)[0]
        self.__logger.info(f"Updating repo at {repo_path}")
        self.__workspace_api.mkdirs(repo_group_path)

        repo_list = self.__repos_api.list(repo_group_path, None).get("repos", [])
        self.__check_duplicated_branches(repo_list)

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
        except RuntimeError:
            self.__logger.info("Repo not found, cloning new repo")
            repo_id = self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]
        else:
            self.__check_correct_project(repo_id, repo_url)
            if force:
                self.__logger.info("Re-cloning repo")
                self.__repos_api.delete(repo_id)
                repo_id = self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]

        try:
            self.__repos_api.update(repo_id=repo_id, branch=branch, tag=tag)
        except HTTPError as e:
            if e.response.json().get("error_code") == "GIT_UNKNOWN_REF":
                self.__logger.info("Error occurred, cleaning up ...")
                self.__repos_api.delete(repo_id)
            raise e
        else:
            self.__logger.info("Repo successfully updated")

    def delete(self, repo_url, repo_name=None, branch=None, tag=None):
        repo_path = self.__resolve_repo_path(repo_name, branch, tag)
        self.__logger.info(f"Deleting repo at {repo_path}")

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
        except RuntimeError:
            self.__logger.info("Repo not found, skipping delete")
        else:
            self.__check_correct_project(repo_id, repo_url)
            self.__repos_api.delete(repo_id)
            self.__logger.info("Repo successfully deleted")

    def __resolve_repo_path(self, repo_name, branch, tag):
        self.__validate_placeholder_arguments("{repo_name}", repo_name, "--repo_name")
        self.__validate_placeholder_arguments("{branch_name}", branch, "--branch")
        self.__validate_placeholder_arguments("{tag_name}", tag, "--tag")
        return self.__repo_base_dir.format(repo_name=repo_name, branch_name=branch, tag_name=tag)

    def __validate_placeholder_arguments(self, placeholder, argument, argument_name):
        if argument is None and placeholder in self.__repo_base_dir:
            raise Exception(f"{placeholder} used in repo.base_dir, but {argument_name} argument was not provided")

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
        except KeyError:
            raise Exception(f"Git provider for {url} not listed.")
