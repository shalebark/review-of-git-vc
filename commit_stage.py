import sys
import Commit
import Index

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

def commit_stage(message):
    iw = Index.IndexWorker()
    iw.load()
    tree = Tree.fromIndex(iw.index)
    tree.save()
    Commit.create(message, tree)
    commit.save()

commit_stage(sys.argv[1])