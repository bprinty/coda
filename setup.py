#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# package setup
# 
# @author <bprinty@gmail.com>
# ------------------------------------------------


# config
# ------
import coda

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


# requirements
# ------------
with open('requirements.txt', 'r') as reqs:
    requirements = map(lambda x: x.rstrip(), reqs.readlines())

test_requirements = [
    'nose==1.3.7',
    'nose-parameterized==0.5.0'
]


# files
# -----
with open('README.rst') as readme_file:
    readme = readme_file.read()


# exec
# ----
setup(
    name='coda',
    version=coda.__version__,
    description='File metadata tagging and organization.',
    long_description=readme,
    author='Blake Printy',
    author_email='bprinty@gmail.com',
    url='https://github.com/bprinty/coda',
    packages=['coda'],
    package_dir={'coda': 'coda'},
    entry_points={
        'console_scripts': [
            'coda = coda.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license='Apache-2.0',
    zip_safe=False,
    keywords=['coda', 'data', 'science', 'analysis', 'file', 'organization', 'metadata'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements
)
