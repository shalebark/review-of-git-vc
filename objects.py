import os

from bio import read, exists
import bio

dirpath = os.path.join('.bvc', 'objects')

# tuple -> (tree-hash, timestamp, commit message)
def commit(ch):
    return tuple(read(os.path.join(dirpath, ch)).split('\n')[0].split('\t'))

# list -> [ (blob-hash, relpath) ]
def tree(th):
    return list(map(lambda l: tuple(l.split('\t')), read(os.path.join(dirpath, th)).split('\n')))

# binary file
def blob(bh):
    return read(os.path.join(dirpath, bh), 'r')

def write(hash, content):
    rp =  '.bvc/objects/' + hash
    if not os.path.exists(rp):
        bio.write(rp, content)

