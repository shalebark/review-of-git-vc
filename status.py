import CONSTANTS
import sys
from pprint import pprint

import Index
import Commit
import Tree

def detect_changes():
    head = Commit.get_commit_head()

    iw = Index.IndexWorker()
    iw.load()
    index = iw.index

    if not head:
        commit_dict = {}
    else:
        commit_dict = Tree.fetch(head.treehash)

    staging_dict = index.as_dict()
    last_dict = commit_dict

    # added
    added = set(staging_dict) - set(last_dict)

    # removed
    removed = set(last_dict) - set(staging_dict)

    # modified
    done = set(list(added) + list(removed))

    modified = [ i[0] for i in set(staging_dict.items()) - set(commit_dict.items()) if i[0] not in done ]

    return (added, removed, modified)

def print_status(label, changes):
    if changes:
        sys.stdout.write(label + ':\n\t')
        sys.stdout.write('\n\t'.join(changes) + '\n')

if __name__ == "__main__":
    changes = detect_changes()

    print_status('Added', changes[0])
    print_status('Removed', changes[1])
    print_status('Modified', changes[2])


