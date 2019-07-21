class PathsPreparer:

    def prepare(self, notebookPaths: list):
        paths = list(map(lambda notebookPath: notebookPath.parts[0:-1], notebookPaths))
        paths = list(set(paths))

        for path in paths:
            for i in range(len(path) - 1):
                x = path[0:i + 1]
                paths.append(x)

        uniquePaths = list(set(paths))
        uniquePaths = sorted(uniquePaths, key=len)

        return list(map(lambda path: '/'.join(path), uniquePaths))
