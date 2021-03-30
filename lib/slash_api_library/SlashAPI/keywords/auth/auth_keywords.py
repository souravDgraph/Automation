# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, W0201, C0301
"""
Author: krishna@dgraph.io
"""

from robot.api import logger
from SlashAPI.components.handlers.auth.auth import Auth

__all__ = ['AuthKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class AuthKeywords:
    """

    Auth Keywords

    """

    @staticmethod
    def login(session_alias,
              base_url,
              header,
              email,
              password,
              expected_response=200):
        logger.info("Login")
        url = base_url + "graphql"
        token = Auth.login(session_alias,
                                           url,
                                 header,
                                           email,
                                           password,
                                           expected_response)
        return token