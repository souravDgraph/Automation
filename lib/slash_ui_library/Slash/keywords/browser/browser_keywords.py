# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SeleniumClient import SeleniumClient


__all__ = ['BrowserKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class BrowserKeywords():
    """Browser related Keyword Library.

    Main operations:

    - open, close, maximize browser
    """

    browsers = dict()
    @staticmethod
    def open_browser(browser_alias, url, browser_name='firefox', remote_url=False,
                     desired_capabilities=None, ff_profile_dir=None,
                     options=None):
        """
        Open the browser and creates a connection alias to the browser object.
        | browser_alias |  alias of the browser |
        | url | url of the page to be launched |
        | browser_name | name of the browser |
        | remote_url | enable remote url Ture/False |
        | desired_capabilities | expected capabilities if any |
        | ff_profile_dir | FF profile directory details |

        Example:
        | Open Browser | browser_1 | https:\\www.google.com | chrome |

        Return:
            None
        """
        _browser = SeleniumClient()
        if browser_name == 'ie' :
            desired_capabilities = {'ie.ensureCleanSession' : True, 'ACCEPT_SSL_CERTS' : True}
        _browser.open_browser(url, browser=browser_name,
                              remote_url=remote_url,
                              desired_capabilities=desired_capabilities,
                              ff_profile_dir=ff_profile_dir,
                              options=options)
        # Maximize Browser Window
        _browser.maximize_browser_window()
        logger.info("Successfully Opened Browser Connection")
        if browser_name == 'ie':
            #value = "document.getElementById('overridelink').click()"
            #_browser.execute_javascript(value)
            _browser.click_element('overridelink')

        BrowserKeywords.browsers[browser_alias] = _browser
        _browser.maximize_browser_window()

    @staticmethod
    def close_browser(browser_alias):
        """
        close the browser and deletes the connection alias and browser object references .
        | browser_alias |  alias of the browser |

        Example:
        | Close Browser | browser_1 |

        Return:
            None
        """
        BrowserKeywords.take_screenshot(browser_alias)
        BrowserKeywords.browsers[browser_alias].close_browser()
        BrowserKeywords.browsers.pop(browser_alias)
        logger.info("Closed Browser")

    @staticmethod
    def switch_browser(browser_alias):
        """
        switches to the browser object based on the connection alias .
        | browser_alias |  alias of the browser |

        Example:
        | Switch Browser | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.browsers[browser_alias]
        return browser

    @staticmethod
    def take_screenshot(browser_alias):
        """

        :param browser_alias:
        :return:
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.capture_page_screenshot()
