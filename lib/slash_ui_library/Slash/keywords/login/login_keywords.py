# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.login.login import LoginLocators
# pylint: disable=too-many-arguments


__all__ = ['LoginKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class LoginKeywords(object):
    """Login Page Keyword Library.

    Main operations:

    - Login and Logout page related operations
    """
    timeout=10
    @staticmethod
    def login(browser_alias, username, password):

        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.input_text(LoginLocators.username, username)
        browser.input_text(LoginLocators.password, password)
        browser.click_element(LoginLocators.continue_button)
