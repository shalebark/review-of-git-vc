import Index

def list_modified():
    iw = Index.IndexWorker()
    iw.load()
    index = iw.index
    return Index.compare_workspace_to_index(index)

import sys
if __name__ == "__main__":
    sys.stdout.writelines('\n'.join(list_modified()))