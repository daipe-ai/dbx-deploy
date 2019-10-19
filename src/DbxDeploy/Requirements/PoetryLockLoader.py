from pathlib import Path
import tomlkit

def loadRequirements(poetryLockPath: Path) -> list:
    requirements = []

    with poetryLockPath.open('r') as t:
        lock = tomlkit.parse(t.read())
        for p in lock['package']:
            if not p['category'] == 'dev':
                requirement = '{}=={}'.format(p['name'], p['version'])
                requirements.append(requirement)

    return requirements
