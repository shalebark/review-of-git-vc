"""
UPDATE_TYPE_CODES:
    0 = ADD
    1 = REMOVE

Updates the index, use the UPDATE_TYPE_CODE to determine wether to add or remove from the index.

TYPE_CODE ADD:
    If the file is already in the index, it will update the virtual file entry.
    If the file is not in the index, it will add a new virtual file entry.
TYPE_CODE REMOVE:
    If the file is already in the index, it will remove it from the virtual file entry.
    If the file is not in the index, it will do nothing.
If a directory is given, it will recursively apply the same code to every file.

"""


import os
import CONSTANTS
import Index

def update_index(filepath, update_type_code):
    iw = Index.IndexWorker()
    iw.load()
    index = iw.index

    if update_type_code is 0:
        index[filepath] = Index.create_index_entry_from_file(filepath)
    else:
        if filepath in index:
            del index[filepath]

    iw.save()

if __name__ == "__main__":
    import sys
    if sys.argv[1] == "add":
        update_type_code = 0
    elif sys.argv[1] == "rm":
        update_type_code = 1
    else:
        update_type_code = -1

    assert(update_type_code is not -1)

    update_index(os.path.relpath(sys.argv[2]), update_type_code)
