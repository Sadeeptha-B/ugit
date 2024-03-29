import argparse
import os
import sys

from . import base
from . import data

def main():
    args = parse_args()
    args.func(args)

def parse_args():
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    # init command
    init_parser = commands.add_parser('init')
    init_parser.set_defaults(func=init)

    # hash-object command
    hash_object_parser = commands.add_parser('hash-object')
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument('file')

    # cat-file command
    cat_file_parser = commands.add_parser('cat-file')
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument('object')

    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)

    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument('tree')

    commit_parser = commands.add_parser('commit')
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('-m', '--message', required=True)

    return parser.parse_args()


# Init function will create .ugit directory. This functionality is separated into data.py
def init(args):
    data.init()
    print(f'Initialized empty ugit repository in {os.path.join(os.getcwd(), data.GIT_DIR)}')


# Save file contents under the hashed name
def hash_object(args):
    with open(args.file, 'rb') as f:
        print(data.hash_object(f.read()))


# Output file contents by hash
def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))

# Stores current directory in the object database. In git lingo a "tree" means a directory
def write_tree(args):
    print(base.write_tree())

def read_tree(args):
    base.read_tree(args.tree)

def commit(args):
    print(base.commit(args.message))