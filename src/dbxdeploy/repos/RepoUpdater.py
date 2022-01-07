from logging import Logger
from requests.exceptions import HTTPError
from databricks_cli.repos.api import ReposApi
from databricks_cli.workspace.api import WorkspaceApi


class RepoUpdater:
    def __init__(
        self,
        logger: Logger,
        repos_api: ReposApi,
        workspace_api: WorkspaceApi,
    ):
        self.__logger = logger
        self.__repos_api = repos_api
        self.__workspace_api = workspace_api

    def create_or_update_branch(self, repo_id: int, branch: str):
        self.__create_or_update(repo_id, branch=branch)

    def create_or_update_tag(self, repo_id: int, tag: str):
        self.__create_or_update(repo_id, tag=tag)

    def __create_or_update(self, repo_id: int, branch: str = None, tag: str = None):
        try:
            self.__repos_api.update(repo_id=repo_id, branch=branch, tag=tag)
        except HTTPError as e:
            if e.response.json().get("error_code") == "GIT_UNKNOWN_REF":
                self.__logger.info("Error occurred, cleaning up ...")
                self.__repos_api.delete(repo_id)
            raise e
