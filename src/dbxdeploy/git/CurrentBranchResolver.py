from dbxdeploy.git.CurrentRepositoryFactory import CurrentRepositoryFactory


class CurrentBranchResolver:
    def __init__(
        self,
        current_repository_factory: CurrentRepositoryFactory,
    ):
        self.__current_repository_factory = current_repository_factory

    def resolve(self) -> str:
        return self.__current_repository_factory.create().head.shorthand
