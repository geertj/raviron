#
# This file is part of ravstack. Ravstack is free software available under
# the terms of the MIT license. See the file "LICENSE" that was provided
# together with this source file for the licensing terms.
#
# Copyright (c) 2015 the ravstack authors. See the file "AUTHORS" for a
# complete list.

import os
from setuptools import setup


version_info = {
    'name': 'ravstack',
    'version': '0.9.6',
    'description': 'Run OpenStack on Ravello',
    'author': 'Geert Jansen',
    'author_email': 'geertj@gmail.com',
    'url': 'https://github.com/geertj/ravstack',
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]
}

topdir, _ = os.path.split(os.path.abspath(__file__))


def get_requirements():
    """Parse a requirements.txt file and return as a list."""
    lines = []
    with open(os.path.join(topdir, 'requirements.txt')) as fin:
        for line in fin:
            lines.append(line.rstrip())
    return lines


if __name__ == '__main__':
    setup(
        packages=['ravstack'],
        package_dir={'': 'lib'},
        install_requires=get_requirements(),
        entry_points={'console_scripts': ['ravstack = ravstack.main:main']},
        **version_info)
