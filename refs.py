import os

from util import read, write, append as io_append
import objects

# returns the current commit-hash
def id():
    return read(os.path.join('.bvc', 'HEAD'))

# commit object using the head hash
# tuple -> (tree-hash, timestamp, commit message)
# if head has not been initialized returns None
def head():
    ch = id()
    if not ch:
        return None
    return objects.commit(ch)

def log():
    lc = read(os.path.join('.bvc', 'refs'))
    return list(map(lambda ch: tuple(read('.bvc/objects/' + ch).split('\t')) + (ch,), [ l.split('\t')[1] for l in lc.split('\n') if l ]))

def common_ancestor(ch1, ch2):
    lc = read(os.path.join('.bvc', 'refs'))
    # (parent_commit, commit)
    ld = [ tuple(l.split('\t')) for l in lc.split('\n') if l ][::-1]

    ah1 = ch1
    ah2 = ch2

    for l in ld:
        if l[1] == ah1:
            ah1 = l[0]
        if l[1] == ah2:
            ah2 = l[0]
        if ah1 == ah2:
            return ah1

    # this should not be possible, as init should be an ancestor to all
    return None

def update_head(ch):
    write(os.path.join('.bvc', 'HEAD'), ch)

# parent_commit new_commit (if no parent_commit, because its init, then use the same hash as the new_commit)
def append(ch):
    pid = id()
    if not pid:
        pid = ch

    io_append(os.path.join('.bvc', 'refs'), pid + '\t' + ch + os.linesep)

