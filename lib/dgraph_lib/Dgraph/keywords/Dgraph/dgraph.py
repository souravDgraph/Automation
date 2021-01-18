"""
Author: krishna@dgraph.io
"""
# pylint: disable=too-many-ancestors

__version__ = "1.0.0"
__all__ = ['Dgraph']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Stagging"

from Dgraph.keywords.custom_request_keywords import CustomRequestKeywords
from Dgraph.keywords.setup_dgraph_keywords import SetupDgraphKeywords


class Dgraph(CustomRequestKeywords, SetupDgraphKeywords):
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
        Dgraph Library consists of Test Rails- for adding-updating-deleting, Custom Requests- for the  and Setup for
        the cli commands.
        """
        print("Dgraph Lib keywords: CustomRequestKeywords, TestRailsKeywords, SetupDgraphKeywords")
