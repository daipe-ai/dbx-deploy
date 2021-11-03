import urllib3
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

    def create_or_update(self, repo_url, branch, tag, repo_name):
        repo_path = self.__repo_path.format(repo_name=repo_name)

        self.__logger.info(f"Trying to update repo at {repo_path}")
        self.__workspace_api.mkdirs(self.__repo_root_dir)

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
            self.__check_for_duplicates()
            self.__check_correct_project(repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, cloning new repo")
            self.__check_for_duplicates(with_branch=branch)
            repo_id = self.__repos_api.create(url=repo_url, provider=self.__get_provider_from_url(repo_url), path=repo_path)["id"]

        self.__repos_api.update(repo_id=repo_id, branch=branch, tag=tag)

        self.__logger.info("Repo successfully updated")

    def delete(self, repo_url, repo_name):
        repo_path = self.__repo_path.format(repo_name=repo_name)

        self.__logger.info(f"Trying to delete repo at {repo_path}")

        try:
            repo_id = self.__repos_api.get_repo_id(repo_path)
            self.__check_correct_project(repo_id, repo_url)
        except RuntimeError:
            self.__logger.info("Repo not found, skipping delete")
        else:
            self.__repos_api.delete(repo_id)
            self.__logger.info("Repo successfully deleted")

        self.__delete_root_dir_if_empty()

    def __check_correct_project(self, repo_id, repo_url):
        repo = self.__repos_api.get(repo_id)
        if repo_url != repo["url"]:
            raise Exception(f"Repo at {repo['path']} has source at {repo['url']}, expected {repo_url}")

    def __check_for_duplicates(self, with_branch: str = None):
        repo_list = self.__repos_api.list(self.__repo_root_dir, None).get("repos", [])
        repo_branches = [repo.get("branch") for repo in repo_list]
        if with_branch:
            repo_branches.append(with_branch)
        branch_counter = [{"name": branch, "count": repo_branches.count(branch)} for branch in set(repo_branches)]
        duplicated_branches = [branch["name"] for branch in branch_counter if branch["count"] > 1]

        if len(duplicated_branches) > 0:
            raise Exception(f"Following branches are/would be duplicated in current env: {', '.join(duplicated_branches)}.")

    def __delete_root_dir_if_empty(self):
        repos = self.__workspace_api.list_objects(self.__repo_root_dir)
        if len(repos) < 1:
            self.__workspace_api.delete(self.__repo_root_dir, is_recursive=False)

    def __get_provider_from_url(self, url):
        provider_map = {
            "github.com": "gitHub",
            "dev.azure.com": "azureDevOpsServices",
        }
        try:
            return provider_map[urllib3.get_host(url)[1]]
        except KeyError:
            raise Exception(f"Git provider for {url} not listed.")
