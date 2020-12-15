#!/usr/bin/env python
"""
Author: vivetha@dgraph.io
"""

from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.keywords.login.login_keywords import LoginKeywords
from Slash.keywords.dashboard.dashboard_keywords import DashboardKeywords
from Slash.keywords.lambdas.lambdas_keywords import LambdaKeywords
from Slash.keywords.settings.settings_keywords import SettingsKeywords
from Slash.keywords.organization.organization_keywords import OrganizationKeywords
from robot.api import logger


# pylint: disable=too-many-ancestors

__version__ = "1.0.0"

__all__ = ['Slash']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Slash(BrowserKeywords,
            LoginKeywords,
            DashboardKeywords,
            OrganizationKeywords,
            LambdaKeywords,
            SettingsKeywords):
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


