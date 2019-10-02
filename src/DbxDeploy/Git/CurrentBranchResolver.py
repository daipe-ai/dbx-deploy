from pygit2 import Repository

class CurrentBranchResolver:

    def resolve(self):
        return Repository('.').head.shorthand
