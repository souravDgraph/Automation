# !/usr/bin/env python

from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='requests_client',
    version=__VERSION__,
    description='Robot Framework test library for api for slash',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    author='Robot Framework Developers',
    author_email='robotframework@gmail.com',
    url='https://github.com/robotframework/SeleniumLibrary',
    license='Apache License 2.0',
    keywords='robotframework testing testautomation requests',
    platforms='any',
    packages=find_packages(),
    requires={
            'install_requires': [
                'robotframework',
                'robotframework-requests'],
    })
