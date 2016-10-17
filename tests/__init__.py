# -*- coding: utf-8 -*-


# imports
# -------
import os
from gems import filetree
import coda


# config
# ------
__tests__ = os.path.dirname(os.path.realpath(__file__))
__resources__ = os.path.join(__tests__, 'resources')


# seed data
# ---------
simple = filetree(os.path.join(__resources__, 'simple'))
source = filetree(os.path.join(__tests__, '..', 'coda'))
fl = []
for item in simple.filelist():
    fl.append(coda.File(path=item, metadata={
        'cohort': 'simple',
        'extension': item.split('.')[-1],
        'type': 'text',
        'base_name': os.path.basename(item),
        'length': len(os.path.basename(item))
    }))
for item in source.prune(r".*.py$").filelist():
    fl.append(coda.File(path=item, metadata={
        'cohort': 'coda',
        'extension': item.split('.')[-1],
        'type': 'source',
        'base_name': os.path.basename(item),
        'length': len(os.path.basename(item))
    }))
cl = coda.Collection(files=fl)


# package-level setUp and tearDown
# --------------------------------
def setUp():
    global __user_config__
    cwd = os.path.dirname(os.path.realpath(__file__))
    coda.db.__user_config__ = os.path.join(cwd, 'resources', '.coda')
    coda.db.options()
    coda.add(cl)
    return


def tearDown():
    coda.delete(cl)
    return


