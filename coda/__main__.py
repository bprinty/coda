# -*- coding: utf-8 -*-
#
# Main entry point for coda script
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# imports
# -------
import os
import sys
from functools import wraps
import argparse
import json
import coda


# decorators
# ----------
def accumulate(func):
    """
    Accumulate all input file arguments into collection.
    """
    @wraps(func)
    def _(args):
        files = []
        for fi in args.files:
            if os.path.isdir(fi):
                cl = coda.Collection(fi)
                files.extend(cl.files)
            else:
                files.append(coda.File(fi))
        args.collection = coda.Collection(files=files)
        return func(args)
    return _


# methods
# -------
def status(args):
    """
    Check status of running databases and configuration.
    """
    sys.stderr.write('\nDatabase configuration:\n')
    opt = coda.db.session.options
    for key in opt:
        sys.stderr.write('    {}: {}\n'.format(key, opt[key]))
    sys.stderr.write('\nTesting connection ... ')
    try:
        coda.find_one({'thisisatest': 'thisisnotatest'})
        sys.stderr.write('good to go!\n\n')
    except:
        sys.stderr.write('could not connect!\n\n')
    return


def find(args):
    """
    Find files with associated keys and metadata.
    """
    cl = coda.find({args.key: args.value})
    if cl is not None:
        sys.stdout.write(str(cl) + '\n')
    return


@accumulate
def show(args):
    """
    Show metadata about tracked file.
    """
    fi = coda.File(args.collection[0].path)
    for fi in args.collection:
        sys.stdout.write('\n' + fi.path + '\n')
        md = fi.metadata.json()
        del md['_id']
        sys.stdout.write(json.dumps(md, sort_keys=True, indent=4) + '\n')
    return


@accumulate
def add(args):
    """
    Add file to internal database for tracking.
    """
    coda.add(args.collection)
    return


@accumulate
def delete(args):
    """
    Delete file from internal database for tracking.
    """
    coda.delete(args.collection)
    return


@accumulate
def tag(args):
    """
    Tag file with metadata.
    """
    args.collection.metadata[args.key] = args.value
    coda.add(args.collection)
    return


# args
# ----
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='Path to config file to use for default coda options.', default=None)
subparsers = parser.add_subparsers()


# version
# -------
parser_version = subparsers.add_parser('version')
parser_version.set_defaults(func=lambda x: sys.exit(coda.__version__))


# status
# ------
parser_status = subparsers.add_parser('status')
parser_status.set_defaults(func=status)


# show
# ----
parser_show = subparsers.add_parser('show')
parser_show.add_argument('files', nargs='+', help='File or collection to list metadata for.')
parser_show.set_defaults(func=show)


# find
# ----
parser_find = subparsers.add_parser('find')
parser_find.add_argument('key', help='Metadata key to search with.')
parser_find.add_argument('value', help='Metadata value to search for.')
parser_find.set_defaults(func=find)


# add
# ---
parser_add = subparsers.add_parser('add')
parser_add.add_argument('files', nargs='+', help='File or collection to add to tracking.')
parser_add.set_defaults(func=add)


# delete
# ------
parser_delete = subparsers.add_parser('delete')
parser_delete.add_argument('files', nargs='+', help='File or collection to add to tracking.')
parser_delete.set_defaults(func=delete)


# tag
# ---
parser_tag = subparsers.add_parser('tag')
parser_tag.add_argument('files', nargs='+', help='File or collection to tag with metadata.')
parser_tag.add_argument('key', help='Metadata key to tag file with.')
parser_tag.add_argument('value', help='Metadata value to tag file with.')
parser_tag.set_defaults(func=tag)


# exec
# ----
def main():
    args = parser.parse_args()
    if args.config:
        coda.db.__user_config__ = args.config
        coda.db.options()
    args.func(args)


if __name__ == "__main__":
    main()

