import re
from pathlib import Path
from typing import Match
from tomlkit import inline_table

class RequirementsLineConverter:

    def parse(self, line: str):
        matches = re.match(r'^([^=]+)==([^;]+)(?:; (.+))?$', line)

        if matches:
            return self.__parseLine(matches)

        matches = re.match(r'^-e git\+(git@[^@]+)@([^#]+)#egg=(.+)$', line)

        if matches:
            return self.__parseGitOldLine(matches)

        matches = re.match(r'^-e git\+(https://(?:[^@]+@)?[^@]+)@([^#]+)#egg=(.+)$', line)

        if matches:
            return self.__parseGitOldLine(matches)

        matches = re.match(r'^([^ ]+) @ git\+(https://(?:[^@]+@)?[^@]+)@([^#]+)(?:#egg=.+)?$', line)

        if matches:
            return self.__parseGitLine(matches)

        matches = re.match(r'^([^ ]+) @ file:///([^;]+)(?:; (.+))?$', line)

        if matches:
            return self.__parseLocalFileLine(matches)

        raise Exception('Invalid requirements.txt line: {}'.format(line))

    def __parseLine(self, matches: Match[str]):
        if matches.group(3) is None:
            return [matches.group(1), matches.group(2).strip()]

        it = inline_table()
        it.append('version', matches.group(2))
        it.append('markers', matches.group(3))

        return [matches.group(1), it]

    def __parseGitOldLine(self, matches: Match[str]):
        it = inline_table()
        it.append('git', matches.group(1))
        it.append('rev', matches.group(2))

        return [matches.group(3), it]

    def __parseGitLine(self, matches: Match[str]):
        it = inline_table()
        it.append('git', matches.group(2))
        it.append('rev', matches.group(3))

        return [matches.group(1), it]

    def __parseLocalFileLine(self, matches: Match[str]):
        filePath = Path(matches.group(2))
        name = matches.group(1)
        version = filePath.name.split('-')[1]
        markers = matches.group(3)

        if markers is None:
            return [name, version]

        it = inline_table()
        it.append('version', version)
        it.append('markers', markers)

        return [name, it]
