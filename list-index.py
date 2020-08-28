import sys
import Index

def list_index():
    iw = Index.IndexWorker()
    iw.load()
    sys.stdout.write(iw.index.__str__())

if __name__ == "__main__":
    list_index()