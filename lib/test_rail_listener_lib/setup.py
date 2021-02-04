#####!/usr/bin/env python
from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='test_rail_listener_lib',
    version=__VERSION__,  # resolved with execfile
    description='Custom Test Rail Listener Library',
    classifiers=[
        'Programming Language :: Python :: 2.x',
        'Programming Language :: Python :: 3.x',
    ],
    author='Krishna Kaushik',
    author_email='tkrishnakaushik96@gmail.io',
    url='https://github.com/robotframework/SSHLibrary',
    license='Apache License 2.0',
    keywords='robotframework dgraph testing',
    platforms='any',
    packages=find_packages(),
    install_requires=['robotframework', 'requests', 'testrail_api'],
)
