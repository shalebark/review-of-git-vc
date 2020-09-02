import os
import math
import hashlib
import binascii
from functools import reduce
from bio import read, write, exists

import objects

INDEX_RELPATH = os.path.join('.bvc', 'INDEX')

# (mtime, size)
def wstat(relpath):
    st = os.stat(relpath)
    return (str(st.st_mtime), str(st.st_size))

def hashbuf(buf):
    hasher = hashlib.sha1()
    bb = bytes(buf, 'utf-8')
    BLOCK_SIZE = 65536
    for i in range(0, math.ceil(len(bb) / BLOCK_SIZE)):
        data = binascii.b2a_hqx(bb[i * BLOCK_SIZE: (i + 1) * BLOCK_SIZE])
        hasher.update(data)
    return hasher.hexdigest()

# blob_hash, rel_path, mtime, size
def read_index():
    bc = read(INDEX_RELPATH)
    if not bc:
        return []
    return list(map(lambda t: t.split('\t'), bc.split('\n')))

# blob_hash, rel_path, mtime, size
def write_index(ri):
    write(INDEX_RELPATH, '\n'.join(map(lambda t: '\t'.join(map(str, t)), ri)))

# adds to stage or the index, if add_to is False, then remove from index instead
def stage(relpath, add_to=True):
    ri = read_index()

    # find the first instance of relpath
    ridx = next(( i for i,j in enumerate(ri) if j[1] == relpath ), None)

    # index structure
    # blob_hash, rel_path, mtime, size
    if add_to:
        bs = wstat(relpath)
        # file is already in the index, it might need to be updated with a new blob, and stats
        if ridx is not None:

            # the file has been updated, update its stats
            if ri[ridx][2] != bs[0] or ri[ridx][2] != bs[0]:
                bc = read(relpath)
                bh = hashbuf(bc)

                # if the blob does not already exists, then create, otherwise, reuse
                if not exists(bh):
                    objects.write(bh, bc)

                ri[ridx] = (bh, relpath, bs[0], bs[1])
        else:
            bc = read(relpath)
            bh = hashbuf(bc)

            # if the blob does not already exists, then create, otherwise, reuse
            if not exists(bh):
                objects.write(bh, bc)
            ri.append((bh, relpath, bs[0], bs[1]))
    else:
        if ridx is not None:
            delete(relpath)
            del ri[ridx]

    # sort the index
    sri = sorted(ri, key=lambda x: x[1])
    write_index(sri)

"""
Finds the 4 statuses ( added to stage, removed from stage, modified tracked files, changed files (added to staging) )
Expects tree contents ( list -> [ (blob-hash, relpath) ] )
"""
def diff_tree_with_index(tree):
    ct = tree
    ri = read_index()

    # retrieves all relpaths
    cif = set(map(lambda x: x[1], ct))
    rif = set(map(lambda x: x[1], ri))

    # (blob_hash, relpath)
    cii = set(map(lambda x: tuple(x[0:2]), ct))
    rii = set(map(lambda x: tuple(x[0:2]), ri))

    # find the added to stage (files that are in stage but not in commit tree)
    added = rif - cif

    # find the removed from stage (files that are in commit tree but not in stage)
    removed = cif - rif

    # files thats been modified and already in index
    staged = set(map(lambda t: t[1], rii - cii)) - added - removed

    # find the modified tracked files
    modified = set()
    for re in ri:
        if re[1] in staged:
            continue
        ws = wstat(re[1])
        if re[2] != ws[0] or re[3] != ws[1]:
            modified.add(re[1])

    # walks through the directory, ignores ./.bvc directory, merges os.walk into relpath, and then strips ./ from the front of each file
    ws = reduce(lambda p,c: c.union(p) ,[ set(map(lambda f: ("%s/%s" %(t[0], f))[2:], t[2])) for t in os.walk('.') if './.bvc' not in t[0][0:6] ], set())
    # relpaths in index
    rf = set(map(lambda x: x[1], ri))
    # untracks are sorted in descending: level of depth in directory (closest to base comes first), a-z
    untracked = sorted(ws - rf, key=lambda x: (x.count('/'), x))

    return (added, removed, staged, modified, untracked)
