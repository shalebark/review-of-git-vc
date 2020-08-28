"""

Files are placed in .bvc directory.
If a .bvc directory is already found, then it is considered to have been initted and will abort.

Terminology Clarfiication:
    The HEAD refers to the current active commit, not the tip.
    The TIP refers to the end of a branch.

.bvc/objects
    Directory for objects
.bvc/logs/HEAD
    Text File listing all heads in descending order.
.bvc/logs/branches/{branch-name}
    Text File listing all heads for a branch in descending order.
.bvc/HEAD
    Text File containing commit-hash of current HEAD
.bvc/INDEX
    Binary File containing INDEX virtual directory pickle
.bvc/tips/{branch-name}
    Text File containing commit-hash to the tip of the branch.

"""

import CONSTANTS
import os
import sys
import shutil

"""
Inits the directory structure. Once initted, the rest of the code can assume that the file is there and not corrupted.
"""
def init():
    assert(not os.path.exists(CONSTANTS.PATH.BASE_DIRECTORY))
    try:
        # .bvc/objects
        os.makedirs(CONSTANTS.PATH.OBJECTS_DIRECTORY)
        # .bvc/logs/branches/{branch-name}
        os.makedirs(CONSTANTS.PATH.BRANCH_HEADS)
        # .bvc/logs/HEAD
        os.mknod(CONSTANTS.PATH.HEADS)
        # .bvc/HEAD
        os.mknod(CONSTANTS.PATH.HEAD)
        # .bvc/INDEX
        os.mknod(CONSTANTS.PATH.INDEX)
        # .bvc/tips/{branch-name}
        os.makedirs(CONSTANTS.PATH.BRANCH_TIP)
    except Exception as err:
        shutil.rmtree(CONSTANTS.PATH.BASE_DIRECTORY)
        raise err
        return False
    return True

if __name__ == "__main__":
    if init():
        sys.stdout.write("BVC initialized.\n")
    else:
        sys.stderr.write("BVC initialize failed.\n")