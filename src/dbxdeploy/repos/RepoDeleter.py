from logging import Logger
from databricks_cli.repos.api import ReposApi


class RepoDeleter:
    def __init__(
        self,
        logger: Logger,
        repos_api: ReposApi,
    ):
        self.__logger = logger
        self.__repos_api = repos_api

    def delete(self, repo_path: str):
        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
        except RuntimeError:
            self.__logger.warn(f"Repo {repo_path} not found, skipping delete")
            return

        self.__repos_api.delete(repo_id)
        self.__logger.info(f"Repo {repo_path} successfully deleted")
