import sys
import Index

def list_index():
    iw = Index.IndexWorker()
    iw.load()
    return str(iw.index)

if __name__ == "__main__":
    sys.stdout.write(list_index())