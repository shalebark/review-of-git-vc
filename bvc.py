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

    # previous head
    pid = refs.id()

    # (branch-name, head-hash)
    bd = current_branch()

    # update head, and ref log
    refs.append(ch)
    refs.update_head(ch)

    # if at the head of a branch, add the commit record to the branch
    if bd is not None and pid == bd[1]:
        append_branch(bd[0], ch)
        util.write(os.path.join('.bvc', 'branch'), bd[0] + '\t' + ch)

# a reference to refs.id
def id():
    return refs.id()

# finds the 4 statuses ( added to stage, removed from stage, staged changes, unstaged changes )
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
    cc = objects.commit(ch)
    tc = objects.tree(cc[0])

    # writes the contents of the tree back to workspace
    for tf in tc:
        util.write(tf[1], objects.blob(tf[0]))

    # update index
    filespace.update_index(tc)

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

def common_ancestor(ch1, ch2):
    return refs.common_ancestor(ch1, ch2)

def current_branch():
    c = util.read(os.path.join('.bvc', 'branch'))
    if not c:
        return None
    return tuple(c.split('\t'))

def make_branch(name):
    # prevent a branch from creating if it already exists
    if util.exists(os.path.join('.bvc', 'branches', name)):
        return

    cc = refs.head()
    hh = util.read(os.path.join('.bvc', 'HEAD')).strip()

    # create a new commit that serves as the root of the branch
    cb = "%s\t%s\t%s" %(cc[0], time.time(), 'Create branch: ' + name)
    ch = filespace.hashbuf(cb)
    objects.write(ch, cb)

    # update the ref log
    refs.append(ch)

    # creates the branches file
    util.write(os.path.join('.bvc', 'branches', name), ch + os.linesep)

def append_branch(name, ch):
    # creates the branch file
    util.append(os.path.join('.bvc', 'branches', name), ch + os.linesep)

def delete_branch(name):
    util.delete(os.path.join('.bvc', 'branches', name))

def checkout_branch(name):
    ch = [ l for l in util.read(os.path.join('.bvc', 'branches', name)).split('\n') if l ][-1]
    util.write(os.path.join('.bvc', 'branch'), name + '\t' + ch)
    refs.update_head(ch)
    checkout(ch)


def init():
    if not os.path.exists('.bvc'):
        os.mkdir('.bvc')
        os.mknod(os.path.join('.bvc', 'HEAD'))
        os.mknod(os.path.join('.bvc', 'INDEX'))
        os.mkdir(os.path.join('.bvc/', 'objects'))
        os.mknod(os.path.join('.bvc', 'refs'))
        os.mkdir(os.path.join('.bvc', 'branches'))
        os.mknod(os.path.join('.bvc', 'branch'))

        commit('initialize')
        make_branch('master')
        checkout_branch('master')

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
    elif method == "branch":
        sys.stdout.write(str(current_branch()) + '\n')
    elif method == "brancha":
        make_branch(sys.argv[2])
    elif method== "branchc":
        checkout_branch(sys.argv[2])
    elif method== "branchd":
        delete_branch(sys.argv[2])
    elif method == "id":
        sys.stdout.write(refs.id() + '\n')
    elif method == "cma":
        sys.stdout.write(common_ancestor(sys.argv[2], sys.argv[3]) + '\n')
    else:
        sys.stderr.write(sys.argv[1] + ' is not an available command.')