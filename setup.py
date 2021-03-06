from setuptools import setup, find_packages
from version import __VERSION__

setup(
    name='dgraph_library',
    version=__VERSION__,  # resolved with execfile
    description='DgraphLib Library',
    classifiers=[
        'Programming Language :: Python :: 2.x',
        'Programming Language :: Python :: 3.x',
    ],
    author='Krishna Kaushik',
    author_email='krishna@dgraph.io',
    url='https://github.com/robotframework/SSHLibrary',
    license='Apache License 2.0',
    keywords='robotframework dgraph testing',
    platforms='any',
    packages=find_packages(),
    install_requires=['robotframework', 'robotframework-seleniumlibrary', 'webdrivermanager', 'testrail_api'],
)
