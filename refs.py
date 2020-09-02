import os

from bio import read
import objects

# commit object using the head hash
# tuple -> (tree-hash, timestamp, commit message)
# if head has not been initialized returns None
def head():
    ch = read(os.path.join('.bvc', 'HEAD'))
    if not ch:
        return None
    return objects.commit(ch)
