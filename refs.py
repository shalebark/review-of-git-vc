import os

from util import read, write, append as io_append
import objects

# commit object using the head hash
# tuple -> (tree-hash, timestamp, commit message)
# if head has not been initialized returns None
def head():
    ch = read(os.path.join('.bvc', 'HEAD'))
    if not ch:
        return None
    return objects.commit(ch)

def log():
    lc = read(os.path.join('.bvc', 'refs'))
    return list(map(lambda ch: tuple(read('.bvc/objects/' + ch).split('\t')) + (ch,), [ l for l in lc.split('\n') if l ]))

def update_head(ch):
    write(os.path.join('.bvc', 'HEAD'), ch)

def append(ch):
    io_append(os.path.join('.bvc', 'refs'), ch + os.linesep)

