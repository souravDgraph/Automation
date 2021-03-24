# !/usr/bin/env python
# coding=utf-8
# pylint: disable=R0903
"""
Author: vivetha@dgraph.io
"""

__all__ = ['LoginLocators']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class LoginLocators:
    """
    Base Locators class for login page
    """

    # User name text box
    username = "xpath = //input[@placeholder='yours@example.com']"
    # password text box
    password = "xpath = //input[@type='password']"
    # continue button
    login_button = "xpath = //input/following::button[text()='Login']"
    logout = "xpath = //div[text()='Log out']"
    profile = "xpath = //div/img[@alt='avatar']"
    ok_button = "xpath = //button[text()='Okay']"
    save_button = "xpath = //button[text()='Save']"
    delete_button = "xpath = //button[text()='Delete']"
    organization = "xpath = //div[text()='Organizations']"
    creation_button = "xpath = //button[text()='Create']"
