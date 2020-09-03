import sys
import os
import time
import functools

import filespace
import objects
import util
import refs

def commit(message):
    ri = filespace.read_index()
    # list of (blob_hash, rel_path)
    ti = sorted([ re[0:2] for re in ri ], key=lambda x: x[0])
    # buffer of the tree
    tb = '\n'.join(map(lambda x: "%s\t%s" %(x[0], x[1]), ti))
    th = filespace.hashbuf(tb)

    # if the tree hash already exists, then an exact copy of the tree already exists, we'll just reuse it, otherwise create the tree object
    if not objects.exists(th):
        objects.write(th, tb)

    # tree hash |  timestamp (seconds from epoch) | message
    # create new commit
    cb = "%s\t%s\t%s" %(th, time.time(), message)
    ch = filespace.hashbuf(cb)
    objects.write(ch, cb)

    # update head, and ref log
    refs.update_head(ch)
    refs.append(ch)

# finds the 4 statuses ( added to stage, removed from stage, modified tracked files, changed files (added to staging) )
def status():
    cc = refs.head()
    # if head has not been initialized, use an empty tree
    tc = objects.tree( cc[0] ) if cc else []
    return filespace.diff_tree_with_index(tc)

"""
# adds to stage or the index, if add_to is False, then remove from index instead
def stage(relpath, add_to=True):
"""
stage = filespace.stage

def checkout(ch):
    cc = list(map(lambda l: l.split('\t'), read('.bvc/objects/' + ch).split('\n')))
    tc = list(map(lambda l: tuple(l.split('\t')), read('.bvc/objects/' + cc[0][0]).split('\n')))

    for tf in tc:
        write(tf[1], read('.bvc/objects/' + tf[0]))

from datetime import datetime
def log():
    ld = refs.log()
    # Jan 01, 1999 - 23:59
    buffer = '\n'.join([ "%s\t%s\t%s" %(j[3], j[2], datetime.fromtimestamp(float(j[1])).strftime('%b %d, %Y %H:%M')) for i, j in enumerate(ld[::-1]) ])
    return buffer

import difflib
def diff(ch1, rp1, ch2, rp2):
    cc1 = objects.commit(ch1)
    cc2 = objects.commit(ch2)

    tc1 = objects.tree(cc1[0])
    tc2 = objects.tree(cc2[0])

    # find the blobhash that matches the filename
    bh1 = next((x[0] for x in tc1 if x[1] == rp1 ))
    bh2 = next((x[0] for x in tc2 if x[1] == rp2 ))

    bc1 = [ l for l in objects.blob(bh1).split('\n') if l ]
    bc2 = [ l for l in objects.blob(bh2).split('\n') if l ]

    return '\n'.join(difflib.unified_diff(bc2, bc1))

def init():
    if not os.path.exists('.bvc'):
        os.mkdir('.bvc')
        os.mknod(os.path.join('.bvc', 'HEAD'))
        os.mknod(os.path.join('.bvc', 'INDEX'))
        os.mkdir(os.path.join('.bvc/', 'objects'))
        os.mknod(os.path.join('.bvc', 'refs'))

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
        if changes[4]:
            print_changes('Untracked', changes[4])

    elif method == "add":
        stage(sys.argv[2], True)
    elif method == "remove":
        stage(sys.argv[2], False)
    elif method == "commit":
        commit(sys.argv[2])
    elif method == "checkout":
        checkout(sys.argv[2])
    elif method == "log":
        sys.stdout.write(log() + '\n')
    elif method == "diff":
        sys.stdout.write(diff('7835afd53f8f6e1795827d10483ac39ff940d973', 'first', '238ba36d6001303be73a061f1f49b5d18ee1f849', 'first') + '\n')
    else:
        sys.stderr.write(sys.argv[1] + ' is not an available command.')