import os
import hashlib

GIT_DIR = '.ugit'

# git init functionality
def init():
    os.makedirs(GIT_DIR)

'''
Each new commit's oid is currently written to the HEAD file in the .ugit directory
'''
def set_HEAD(oid):
    with open(os.path.join(GIT_DIR, 'HEAD'), 'w') as f:
        f.write(oid)
    

def hash_object(data, type_="blob"):
    # The type of the file content and a null byte is prepended to the file
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()

    filepath = os.path.join(GIT_DIR, 'objects', oid)  # .ugit/objects/oid
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as out:
        out.write(obj)

    return oid

def get_object(oid, expected="blob"):
    path = os.path.join(GIT_DIR, 'objects', oid)  # .ugit/objects/oid
    with open(path, 'rb') as f:
        obj =  f.read()

    type_, _, content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected != type_:
        raise ValueError(f'Expected {expected}, got {type_}')
    return content