from tomlkit import inline_table
from tomlkit.items import Table

class Lock2PyprojectConverter:

    def convert(self, dependency: Table):
        if 'source' in dependency:
            source: Table = dependency['source']

            if source['type'] == 'git':
                return dependency['name'], self.__getGitSource(source)

            raise Exception(f'Unexpected dependency source type: {source["type"]}')

        return self.__getStandardDependency(dependency)

    def __getStandardDependency(self, dependency: Table):
        it = inline_table()

        if 'marker' in dependency:
            it.append('version', dependency['version'])
            it.append('markers', dependency['marker'])

            return dependency['name'], it

        return dependency['name'], dependency['version']

    def __getGitSource(self, source: Table):
        it = inline_table()
        it.append('git', source['url'])
        it.append('rev', source['reference'])

        return it
