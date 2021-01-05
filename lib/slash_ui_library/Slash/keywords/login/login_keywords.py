# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""


from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.login.login import LoginLocators



__all__ = ['LoginKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class LoginKeywords():
    """Login Page Keyword Library.

    Main operations:

    - Login and Logout page related operations
    """
    timeout = 10

    @staticmethod
    def login(browser_alias, username, password):
        """
        Log into Slash with the username and password provided

        | browser_alias | Alias of the browser on which webdriver should do actions |
        | username | Username for slash |
        | password | Password for slash |

        Example:
            Login    Browser1    user    password
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.input_text(LoginLocators.username, username)
        browser.input_text(LoginLocators.password, password)
        browser.click_element(LoginLocators.continue_button)

    @staticmethod
    def click_organizations_in_profile(browser_alias):
        """
        Click Organizations in the profile drop down menu

        | browser_alias | Alias of the browser on which webdriver should do actions |

        Example:
            Click Organizations In Profile    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LoginLocators.profile)
        browser.click_element(LoginLocators.organization)

    @staticmethod
    def logout(browser_alias):
        """
        Log out of Slash

        | browser_alias | Alias of the browser on which webdriver should do actions |

        Example:
            Logout    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LoginLocators.profile)
        browser.click_element(LoginLocators.logout)

    @staticmethod
    def click_ok_button(browser_alias):
        """
        Click Ok Button

        | browser_alias | Alias of the browser on which webdriver should do actions |

        Example:
            Click Ok Button    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LoginLocators.ok_button)
