import hashlib
import binascii
import CONSTANTS

def hash(filepath):
    hasher = hashlib.sha1()

    with open(filepath, 'rb') as f:
        BLOCK_SIZE = 65536 #64kb chunks
        buff = f.read(BLOCK_SIZE)

        while(len(buff) > 0):
            data = binascii.b2a_hqx(buff)
            hasher.update(data)
            buff = f.read(BLOCK_SIZE)

    return hasher.hexdigest()

def is_stored(hashid):
    return os.path.exists(CONSTANTS.PATH.OBJECTS_DIRECTORY + hashid)

def store_file(filepath):
    hashid = hash(filepath)
    bc = None
    with open(filepath, 'r') as f:
        bc = f.read()
    with open(CONSTANTS.PATH.OBJECTS_DIRECTORY + hashid, 'w') as f:
        f.write(bc)
    return hashid

def contents(hashid):
    bc = None
    with open(CONSTANTS.PATH.OBJECTS_DIRECTORY + hashid, 'r') as f:
        bc = f.read()
    return bc
