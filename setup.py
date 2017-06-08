#!/usr/bin/env python3

from setuptools import setup, find_packages

def read_file(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read()

setup(
    name='overview_upload',
    version='0.9.4',
    description='Upload documents to Overview web server',
    long_description=read_file('README.rst'),
    url='https://github.com/overview/overview-upload-directory',
    install_requires=read_file('requirements.txt').splitlines(),
    packages=[ 'overview_upload' ],
    scripts=[ 'overview-upload', 'overview-upload-csv' ],
    classifiers=(
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    )
)
