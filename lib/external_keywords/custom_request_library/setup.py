#####!/usr/bin/env python
from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='request_handler_library',
    version=__VERSION__,  # resolved with execfile
    description='Request Handler Library',
    classifiers=[
        'Programming Language :: Python :: 2.x',
        'Programming Language :: Python :: 3.x',
    ],
    author='Kaushik',
    author_email='tkrishnakaushik96@gmail.io',
    url='https://github.com/robotframework/SSHLibrary',
    license='Apache License 2.0',
    keywords='robotframework dgraph testing',
    platforms='any',
    packages=find_packages(),
    install_requires=['robotframework','requests'],
)
