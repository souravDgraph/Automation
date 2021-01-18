"""
Author: krishna@dgraph.io
"""
# pylint: disable=too-many-ancestors

__version__ = "1.0.0"
__all__ = ['Common']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Stagging"

from Common.keywords.test_rails_keywords import TestRailsKeywords
from Common.keywords.pydgraph_keywords import PydgraphKeywords


class Common(TestRailsKeywords, PydgraphKeywords):
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
        print('Dgraph Library')

    def about(self):
        """
        Common Library consists of Keywords related to both Slash and Dgraph
        """
        print("Common Lib keywords: TestRailsKeywords, PydgraphKeywords")
