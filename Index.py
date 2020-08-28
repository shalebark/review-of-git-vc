import pickle
import CONSTANTS
import blob
import os

from sortedcontainers import SortedDict
"""
IndexEntry:
    {`st_mode`} {`st_mtime`} {`st_uid`} {`st_size`} {blob-hash} {staging-number} {file-path}
    {`st_mode`} is the file type and mode represented in 4 3 byte digits (ex: 0777)
    {`st_mtime`} is last modified time of the file.
    {`st_uid`} is the uid of the owner
    {`st_size`} is the size of the file
    {blob-hash} a link to the hash
    {staging-number} is the staging number of the file, default is 0.
    {file-path} is the filepath
"""
class IndexEntry:
    #='0000000000000000000000000000000000000000'
    def __init__(self, mode, mtime, uid, size, blob_hash, staging_number, file_path):
        self.mode = mode
        self.mtime = mtime
        self.uid = uid
        self.size = size
        self.blob_hash = blob_hash
        self.staging_number = staging_number
        self.file_path = file_path

    def changed(self, other) -> bool:
        if type(other) is os.stat_result:
            return  self.mode == other.st_mode and self.mtime == other.st_mtime and self.size == other.st_size
        return False

    def compare(self, other):
        return not self.changed(other)

    def __str__(self):
        return "%s %s %s %s %s %s %s %s" %(self.mode, self.mtime, self.uid, self.size, self.size, self.blob_hash, self.staging_number, self.file_path)

class Index:
    def __init__(self):
        self.entries = SortedDict()
        self.__iter_current = None

    def __contains__(self, x):
        return x in self.entries

    def __setitem__(self, filepath: str, value: IndexEntry):
        self.entries[filepath] = value

    def __delitem__(self, filepath: str):
        del self.entries[filepath]

    def __str__(self):
        return '\n'.join(map(lambda x: str(x), self))

    def __iter__(self):
        self.__entries_iter = iter(self.entries)
        return self

    def __next__(self):
        return self.entries[next(self.__entries_iter)]

class IndexWorker:
    def __init__(self):
        self.__handle = None

    def __del__(self):
        if self.__handle:
            self.__handle.close()

    def load(self):
        if self.__handle is None:
            self.__handle = open(CONSTANTS.PATH.INDEX, 'rb+')

        if os.stat(CONSTANTS.PATH.INDEX).st_size is 0:
            self.index = Index()
            return

        self.index = pickle.load(self.__handle)

    def save(self):
        if self.__handle is None:
            self.__handle = open(CONSTANTS.PATH.INDEX, 'rb+')

        self.__handle.seek(0)
        pickle.dump(self.index, self.__handle)

"""
    Adds a new entry to the index.
    The file must exist, and the file must be new to the index (not currently in the index).
"""
def create_index_entry_from_file(relpath: str) -> IndexEntry:
    stat = os.stat(relpath)
    hashid = blob.store_file(relpath)
    return IndexEntry(stat.st_mode, stat.st_mtime, stat.st_uid, stat.st_size, hashid, 0, relpath)

def compare_filepath_to_index(index: Index, relpath: str) -> bool:
    stat = os.stat(relpath)
    return entry.compare(stat)

def compare_workspace_to_index(index: Index) -> list:
    return [ entry.file_path for entry in index if entry.compare(os.stat(entry.file_path)) ]
