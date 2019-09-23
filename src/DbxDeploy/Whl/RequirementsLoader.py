def loadRequirements(fname: str):
    with open(fname) as f:
        return f.read().strip().split('\n')
