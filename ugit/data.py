import os
import hashlib

GIT_DIR = '.ugit'

# git init functionality
def init():
    os.makedirs(GIT_DIR)

def hash_object(data):
    oid = hashlib.sha1(data).hexdigest()
    path = os.path.join(GIT_DIR, 'objects', oid)  # .ugit/objects/oid

    with open(path, 'wb') as out:
        out.write(data)

    return oid

def get_object(oid):
    path = os.path.join(GIT_DIR, 'objects', oid)  # .ugit/objects/oid
    with open(path, 'rb') as f:
        return f.read()