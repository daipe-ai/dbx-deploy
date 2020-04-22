from dbxdeploy.git.CurrentRepositoryFactory import CurrentRepositoryFactory

class CurrentBranchResolver:

    def __init__(
        self,
        currentRepositoryFactory: CurrentRepositoryFactory,
    ):
        self.__currentRepositoryFactory = currentRepositoryFactory

    def resolve(self) -> str:
        return self.__currentRepositoryFactory.create().head.shorthand
