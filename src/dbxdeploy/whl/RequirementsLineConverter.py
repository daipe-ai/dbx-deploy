import re
from tomlkit import inline_table

class RequirementsLineConverter:

    def parse(self, line: str):
        matches = re.match(r'^([^=]+)==([^;]+)(?:; (.+))?$', line)

        if not matches:
            raise Exception('Invalid requirements.txt line: {}'.format(line))

        if matches.group(3) is None:
            return [matches.group(1), matches.group(2).strip()]

        it = inline_table()
        it.append('version', matches.group(2))
        it.append('markers', matches.group(3))

        return [matches.group(1), it]
