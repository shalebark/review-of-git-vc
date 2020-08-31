from sortedcontainers import SortedDict

def fetch(hash: str) -> dict:
    tree = {}
    with open(CONSTANTS.PATH.OBJECTS_DIRECTORY + treehash) as f:
        for line in f.readlines():
            toks = line.split('\t')
            blobhash = toks[0]
            relpath = toks[1]
            tree[relpath]  = (blobhash, relpath)
    return tree