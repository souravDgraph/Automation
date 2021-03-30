# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SlashAPI.components.client.client import Connection
from SlashAPI.components.handlers.utils.utils import Utils
from SlashAPI.components.models.auth.auth import AuthModels
import requests, time

__all__ = ['Auth']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Auth():
    """

    """

    @staticmethod
    def login(session_alias,
              url,
              header,
              username,
              password,
              expected_response=200):

        properties = {
            "email": username,
            "password": password

        }
        data = Utils.render_data_from_template(AuthModels.login,
                                               properties)
        logger.info(data)
        connection = Connection()
        connection.create_session(session_alias, url, header)
        response = connection.post_on_session(session_alias, '',
                                              headers=header,
                                              json=data,
                                              expected_status=str(expected_response))

        logger.info(response.json())
        data = response.json()
        return data["data"]["login"]["token"]



