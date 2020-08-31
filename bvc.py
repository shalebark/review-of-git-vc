
import sys
import hashlib
import binascii
import math
import os
import time
import CONSTANTS

def hashbuf(buf):
    hasher = hashlib.sha1()
    bb = bytes(buf, 'utf-8')
    BLOCK_SIZE = 65536
    for i in range(0, math.ceil(len(bb) / BLOCK_SIZE)):
        data = binascii.b2a_hqx(bb[i * BLOCK_SIZE: (i + 1) * BLOCK_SIZE])
        hasher.update(data)
    return hasher.hexdigest()

def read(relpath):
    with open(relpath, 'r') as f:
        return f.read()

# (mtime, size)
def wstat(relpath):
    st = os.stat(relpath)
    return (str(st.st_mtime), str(st.st_size))

# make and write to file, always truncate file first
def write(relpath, content):
    with open(relpath, 'w') as f:
        f.write(content)

def remove(relpath):
    if exists(relpath):
        os.remove(relpath)

def exists(relpath):
    return os.path.exists(relpath)

# blob_hash, rel_path, mtime, size
def read_index():
    bc = read('.bvc/INDEX')
    if not bc:
        return []
    return list(map(lambda t: t.split('\t'), bc.split('\n')))

# blob_hash, rel_path, mtime, size
def write_index(ri):
    write('.bvc/INDEX', '\n'.join(map(lambda t: '\t'.join(map(str, t)), ri)))

def commit(message):
    ri = read_index()
    # list of (blob_hash, rel_path)
    ti = sorted([ re[0:2] for re in ri ], key=lambda x: x[0])
    # buffer of the tree
    tb = '\n'.join(map(lambda x: "%s\t%s" %(x[0], x[1]), ti))
    th = hashbuf(tb)
    # if the tree hash already exists, then an exact copy of the tree already exists, we'll just reuse it, otherwise create the tree object
    if not exists('.bvc/objects/' + th):
        write('.bvc/objects/' + th, tb)
    # tree hash |  timestamp (seconds from epoch) | message
    cb = "%s\t%s\t%s" %(th, time.time(), message)
    ch = hashbuf(cb)
    write('.bvc/objects/' + ch, cb)
    write('.bvc/HEAD', ch)

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
                    write('.bvc/objects/' + bh, bc)

                ri[ridx] = (bh, relpath, bs[0], bs[1])
        else:
            bc = read(relpath)
            bh = hashbuf(bc)

            # if the blob does not already exists, then create, otherwise, reuse
            if not exists(bh):
                write('.bvc/objects/' + bh, bc)
            ri.append((bh, relpath, bs[0], bs[1]))
    else:
        if ridx is not None:
            remove(relpath)
            del ri[ridx]

    # sort the index
    sri = sorted(ri, key=lambda x: x[1])
    write_index(sri)

def read_commit_tree():
    # reads the HEAD, then reads the commit, then reads the tree of the commit and then converts it to a list
    hh = read('.bvc/HEAD')
    if not hh:
        return []
    ch = read('.bvc/objects/' + hh).split('\t')[0]
    return list(map(lambda l: l.split('\t'), read('.bvc/objects/' + ch).split('\n')))

# finds the 4 statuses ( added to stage, removed from stage, modified tracked files, changed files (added to staging) )
def status():
    ct = read_commit_tree()
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

    return (added, removed, staged, modified)

def checkout(ch):
    cc = list(map(lambda l: l.split('\t'), read('.bvc/objects/' + ch).split('\n')))
    tc = list(map(lambda l: tuple(l.split('\t')), read('.bvc/objects/' + cc[0][0]).split('\n')))

    for tf in tc:
        write(tf[1], read('.bvc/objects/' + tf[0]))

def init():
    if not exists('.bvc'):
        os.mkdir('.bvc')
        os.mknod('.bvc/HEAD')
        os.mknod('.bvc/INDEX')
        os.mkdir('.bvc/objects')

if __name__ == "__main__":
    method = sys.argv[1]
    if method == "init":
        init()
    elif method == "status":
        def print_changes(label, relpaths):
            sys.stdout.write(label + ':\n\t' + '\n\t'.join(relpaths) + '\n')
        changes = status()
        if changes[0]:
            print_changes('Added', changes[0])
        if changes[1]:
            print_changes('Removed', changes[1])
        if changes[2]:
            print_changes('Staged', changes[2])
        if changes[3]:
            print_changes('Unstaged changes', changes[3])

    elif method == "add":
        stage(sys.argv[2], True)
    elif method == "remove":
        stage(sys.argv[2], False)
    elif method == "commit":
        commit(sys.argv[2])
    elif method == "checkout":
        checkout(sys.argv[2])
    else:
        sys.stderr.write(sys.argv[1] + ' is not an available command.')