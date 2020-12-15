# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from robot.api.deco import keyword
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.lambdas.lambdas import LambdaLocators
from time import sleep



__all__ = ['LambdaKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class LambdaKeywords(object):
    """Dashboard/Landing Page Keyword Library.

    Main operations:

    - create Backend.
    """
    timeout = 10

    @staticmethod
    def fill_lambda_script(browser_alias, lambda_script):
        browser = BrowserKeywords.switch_browser(browser_alias)
        js = 'document.getElementsByClassName("' + LambdaLocators.lambda_script + '").innerText= "' + lambda_script + '"'
        logger.info(js)
        browser.execute_javascript(js)

    @staticmethod
    def click_save_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.save_button)








        
        

