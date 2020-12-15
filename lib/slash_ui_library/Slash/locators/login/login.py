# !/usr/bin/env python
# coding=utf-8
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

    #User name text box
    username = "username"
    #password text box
    password = "password"
    #continue button
    continue_button = "action"
    logout = "xpath = //div[text()='Log out']"
    profile = "xpath = //div/img[@alt='avatar']"
    ok_button = "xpath = //button[text()='Okay']"
    save_button = "xpath = //button[text()='Save']"
    delete_button = "xpath = //button[text()='Delete']"
    organization = "xpath = //div[text()='Organizations']"
    creation_button = "xpath = //button[text()='Create']"
