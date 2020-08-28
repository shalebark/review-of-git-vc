"""
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

Directory Paths are / trailing

"""

class PATH:
    BASE_DIRECTORY = "./.bvc"
    OBJECTS_DIRECTORY = ".bvc/objects/"
    HEADS = ".bvc/logs/HEAD"
    BRANCH_HEADS = ".bvc/logs/branches/"
    HEAD = ".bvc/HEAD"
    INDEX = ".bvc/INDEX"
    BRANCH_TIP = ".bvc/tips/"
