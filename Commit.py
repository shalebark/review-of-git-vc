import status
import CONSTANTS
from typing import Optional

class Commit:
    def __init__(self, hash, treehash, message):
        self.hash = treehash
        self.treehash = treehash
        self.message = message

def fetch(hash : str) -> Commit:
    with open(CONSTANTS.PATH.OBJECTS_DIRECTORY + hash) as f:
        content = f.read()
        sep = content.find(' ')
        treehash = content[0:sep]
        message = content[sep:]
        return Commit(hash, treehash, message)

def get_commit_head() -> Optional[Commit]:
    head = ''
    with open(CONSTANTS.PATH.HEAD, 'r') as f:
        head = f.read()
    if not head:
        return None
    return fetch(head)

