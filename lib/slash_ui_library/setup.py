"""
Slash UI Library Setup File.
"""
from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='slash_ui_library',
    version=__VERSION__,  # resolved with execfile
    description='Slash UI Library',
    classifiers=[
        'Programming Language :: Python :: 2.x',
        'Programming Language :: Python :: 3.x',
    ],
    author='Vivetha',
    author_email='vivetha@dgraph.io',
    url='https://github.com/robotframework/SSHLibrary',
    license='Apache License 2.0',
    keywords='robotframework slash testing',
    platforms='any',
    packages=find_packages(),
    install_requires=['robotframework', 'robotframework-seleniumlibrary'],
)
