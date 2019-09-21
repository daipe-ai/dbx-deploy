from pip._internal.req import parse_requirements

def loadRequirements(fname):
    reqs = parse_requirements(fname, session='test')
    return [str(ir.req) for ir in reqs]
