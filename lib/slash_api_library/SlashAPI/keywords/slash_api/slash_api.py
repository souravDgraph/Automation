#!/usr/bin/env python
# pylint: disable=no-self-use
"""
Author: vivetha@dgraph.io
"""

from SlashAPI.keywords.deployemnts.deployment_keywords import DeploymentKeywords
from SlashAPI.keywords.organizations.organizations_keywords import OrganizationsKeywords

# pylint: disable=too-many-ancestors

__version__ = "1.0.0"

__all__ = ['SlashAPI']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class SlashAPI(DeploymentKeywords, OrganizationsKeywords):
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
        print('Slash Keyword Library')

    def about(self):
        """ Just a placeholder function printing the library description
        """
        print('Robot Networker Core Keyword Library derrived from all '
              ' component level keyword libraries, serves as single access'
              ' for all networker keywords')
