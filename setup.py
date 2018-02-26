#!/usr/bin/env python

import io

from setuptools import setup, find_packages

readme = io.open('README.md').read()

setup(
    name='logx',
    version='0.1.1519641991',
    url='https://github.com/djrobstep/logx',
    description='best practice python logging with zero config',
    long_description=readme,
    author='Robert Lechte',
    author_email='robertlechte+djrobstep@gmail.com',
    install_requires=[
        'logging_tree',
        'pyyaml'
    ],
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
