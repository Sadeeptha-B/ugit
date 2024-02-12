import os
from .  import data

# Basic Higher level logic of ugit


'''
Adds files and folders to the object database recursively. A folder with cats.txt, dogs.txt, other/
will be represented by,

blob 91a7b14a584645c7b995100223e65f8a5a33b707 cats.txt
blob fa958e0dd2203e9ad56853a3f51e5945dad317a4 dogs.txt
tree 53891a3c27b17e0f8fd96c058f968d19e340428d other
'''
def write_tree(directory='.'):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = os.path.join(directory, entry.name)
            if is_ignored(full):
                continue

            if entry.is_file(follow_symlinks=False):
                #Write the file to object store
                type_ = 'blob'
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)

            entries.append((entry.name, oid, type_))

    # Create the tree object
    tree = ''.join(f'{type_} {oid} {name}\n'
                   for name, oid, type_
                   in sorted(entries))
    
    return data.hash_object(tree.encode(), 'tree')


def read_tree(tree_oid):
    _empty_current_directory()
    for path, oid in get_tree(tree_oid, base_path='.').items():
        os.makedirs(os.path.dirname(path), exist_ok = True)
        with open(path, 'wb') as f:
            f.write(data.get_object(oid))

'''
Uses iterator to recursively parse tree entries into a dictionary
'''
def get_tree(oid, base_path=''):
    result = {}
    for type_, oid, name in _iter_tree_entries(oid):
        
        assert name not in ('..', '.')

        path = os.path.join(base_path, name)
        if type_ == 'blob':
            result[path] = oid
        elif type == 'tree':
            # Return val
            result.update(get_tree(oid, path))
        else:
            raise ValueError(f'Unknown tree entry {type_}')

    return result

'''Iterator'''
def _iter_tree_entries(oid):
    if not oid:
        return
    
    # Content in bytes
    tree = data.get_object(oid, 'tree')

    # Return file contents, line by line as sequence
    for entry in tree.decode().splitlines():
        type_, oid, name = entry.split(' ', 2)
        yield type_, oid, name

def is_ignored(path):
    return '.ugit' in os.path.split(path)


def _empty_current_directory():
    # Goes through the files and directories bottom up first
    for root, dirnames, filenames in os.walk('.', topdown=False):
        for filename in filenames:
            path = os.path.relpath(os.path.join(root, filename))
            if is_ignored(path) or not os.path.isfile(path):
                continue
            os.remove(path)
        
        for dirname in dirnames:
            path = os.path.relpath(os.path.join(root, dirname))
            if is_ignored(path):
                continue
            try:
                # Since the traversal happens bottom up, no files are missed. 
                os.rmdir(path)
            except (FileNotFoundError, OSError):
                # Deletion might fail if the directory contains unremoved files; i.e. ignored files
                # That is fine
                pass