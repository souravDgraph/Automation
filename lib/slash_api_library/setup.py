#####!/usr/bin/env python
from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='slash_api_library',
    version=__VERSION__,  # resolved with execfile
    description='Slash API Library',
    classifiers=[
        'Programming Language :: Python :: 2.x',
        'Programming Language :: Python :: 3.x',
    ],
    author='Vivetha',
    author_email='vivetha@dgraph.io',
    url='https://github.com/MarketSquare/robotframework-requests',
    license='Apache License 2.0',
    keywords='robotframework slash api testing',
    platforms='any',
    packages=find_packages(),
    install_requires=['robotframework', 'robotframework-requests', 'Jinja2'],
)
