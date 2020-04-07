import re
from typing import Match
from tomlkit import inline_table

class RequirementsLineConverter:

    def parse(self, line: str):
        matches = re.match(r'^([^=]+)==([^;]+)(?:; (.+))?$', line)

        if matches:
            return self.__parseLine(matches)

        matches = re.match(r'^-e git\+(git@[^@]+)@([^#]+)#egg=(.+)$', line)

        if matches:
            return self.__parseGitLine(matches)

        raise Exception('Invalid requirements.txt line: {}'.format(line))

    def __parseLine(self, matches: Match[str]):
        if matches.group(3) is None:
            return [matches.group(1), matches.group(2).strip()]

        it = inline_table()
        it.append('version', matches.group(2))
        it.append('markers', matches.group(3))

        return [matches.group(1), it]

    def __parseGitLine(self, matches: Match[str]):
        it = inline_table()
        it.append('git', matches.group(1))
        it.append('rev', matches.group(2))

        return [matches.group(3), it]
