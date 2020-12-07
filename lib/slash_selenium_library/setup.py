# !/usr/bin/env python

from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='slash_selenium_library',
    version=__VERSION__,
    description='Robot Framework test library for Selenium for Networker',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    author='Robot Framework Developers',
    author_email='robotframework@gmail.com',
    url='https://github.com/robotframework/SeleniumLibrary',
    license='Apache License 2.0',
    keywords='robotframework testing testautomation selenium',
    platforms='any',
    packages=find_packages(),
    requires={
            'install_requires': [
                'robotframework',
                'robotframework-seleniumlibrary'],
    })
