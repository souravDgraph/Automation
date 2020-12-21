"""
Author: tkrishnakaushik96@gmail.com
"""
# pylint: disable=too-many-ancestors

__version__ = "1.0.0"
__all__ = ['Dgraph']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "tkrishnakaushik96@gmail.com"
__status__ = "Stagging"

from Dgraph.keywords.custom_request_keywords import CustomRequestKeywords
from Dgraph.keywords.test_rails_keywords import TestRailsKeywords


class Dgraph(CustomRequestKeywords, TestRailsKeywords):
    """Robot Framework Slash GraphQL Keyword Library.
    All the keywords pertaining to Networker are
    exposed to the user through this library.
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    ROBOT_CODE_ROOT_FOLDER_PATH = None
    ROBOT_CODE_BRANCH_FOLDER_PATH = None
    ROBOT_CODE_UTILS_FOLDER_PATH = None
    OS = None

    def __init__(self):
        """
        Framework init
        Initializes framework properties such as absolute code path
        """
        print('lib Keyword Library')

    def about(self):
        """ Just a placeholder function printing the library description
        """
        print('Robot Networker Core Keyword Library derrived from all '
              ' component level keyword libraries, serves as single access'
              ' for all networker keywords')