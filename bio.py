import os

def read(relpath, mode='r'):
    with open(relpath, mode) as f:
        return f.read()

# make and write to file, always truncate file first
def write(relpath, content, mode='w'):
    with open(relpath, 'w') as f:
        f.write(content)

def delete(relpath):
    if exists(relpath):
        os.remove(relpath)

# makes and appends to file, always appends
def append(relpath, content):
    return write(relpath, content, 'a')

def exists(relpath):
    return os.path.exists(relpath)