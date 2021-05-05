# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring, unused-import
"""
Author: vivetha@dgraph.io
"""

import re, time
from robot.api import logger
from robot.api.deco import keyword
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.lambdas.lambdas import LambdaLocators
from selenium.webdriver.common.keys import Keys

__all__ = ['LambdaKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class LambdaKeywords:
    """Dashboard/Landing Page Keyword Library.

    Main operations:

    - create Backend.
    """
    timeout = 10

    @staticmethod
    def fill_lambda_script(browser_alias, lambda_script):
        """
        fill lambda script
        | browser_alias |  alias of the browser |
        | lambda_script | lambda script |

        Example:
        | Fill Lambda Script | browser_1 | async function({}) |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        time.sleep(15)
        browser.wait_until_page_contains_element(LambdaLocators.lambda_script, timeout=LambdaKeywords.timeout)
        browser.get_webelement(LambdaLocators.lambda_script).send_keys("async function")
        browser.get_webelement(LambdaLocators.lambda_script).send_keys(Keys.DELETE)
        #browser.clear_element_text(LambdaLocators.lambda_script)
        #browser.input_password(LambdaLocators.lambda_script, "async")
        #browser.input_text(LambdaLocators.lambda_script, "async")
        #browser.wait_until_page_contains_element(LambdaLocators.lambda_comment, timeout=LambdaKeywords.timeout)

    @staticmethod
    def click_save_button(browser_alias):
        """
        click save button
        | browser_alias |  alias of the browser |

        Example:
        | Click Save Button | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.save_button, timeout=LambdaKeywords.timeout)

    @staticmethod
    def click_refresh_button(browser_alias):
        """
        click refresh button
        | browser_alias |  alias of the browser |

        Example:
        | Click Refresh Button | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.refresh_button, timeout=LambdaKeywords.timeout)

    @staticmethod
    def click_download_button(browser_alias):
        """
        click download button
        | browser_alias |  alias of the browser |

        Example:
        | Click Download Button | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.download_button, timeout=LambdaKeywords.timeout)

    @staticmethod
    def click_logs_tab(browser_alias):
        """
        click logs tab
        | browser_alias |  alias of the browser |

        Example:
        | Click Logs Tab | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.logs_tab, timeout=LambdaKeywords.timeout)
        browser.wait_until_page_contains_element(LambdaLocators.refresh_button, timeout=LambdaKeywords.timeout)

    @staticmethod
    def click_script_tab(browser_alias):
        """
        click script tab
        | browser_alias |  alias of the browser |

        Example:
        | Click Script Tab | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.script_tab, timeout=LambdaKeywords.timeout)
        browser.wait_until_page_contains_element(LambdaLocators.delete_button, timeout=LambdaKeywords.timeout)

    @staticmethod
    def click_delete_button(browser_alias):
        """
        click delete button
        | browser_alias |  alias of the browser |

        Example:
        | Click Delete Button | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.delete_button, timeout=LambdaKeywords.timeout)
        browser.click_element(LambdaLocators.popup_delete_button, timeout=LambdaKeywords.timeout)

    @staticmethod
    def change_filter(browser_alias, current_filter, new_filter):
        """
        check filter in the lambda logs
        | browser_alias |  alias of the browser |
        | current_filter | present filter in lambda logs |
        | new_filter | new filter for the lambda logs | 

        Example:
        | Change Filter | browser_1 | Last 15 minutes | Last 30 minutes |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(LambdaLocators.filter_button.replace("%s", current_filter), timeout=LambdaKeywords.timeout)
        browser.click_element(LambdaLocators.filter_button.replace("%s", new_filter), timeout=LambdaKeywords.timeout)
        browser.wait_until_page_contains_element(LambdaLocators.filter_button.replace("%s", new_filter), timeout=LambdaKeywords.timeout)
    
    @staticmethod
    def get_lambda_script(browser_alias):
        """
        get lambda script
        | browser_alias |  alias of the browser |

        Example:
        | Get Lambda Script | browser_1 |

        Return:
            lambda script
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        js_exe = LambdaLocators.get_lambdas
        lambdas = browser.execute_javascript(js_exe)
        lambdas = re.sub('[0-9,\n, \u200b]', '', lambdas)
        logger.info(lambdas)
        return lambdas

    @staticmethod
    def check_lambda_logs_present(browser_alias):
        """
        check lambda logs present
        | browser_alias |  alias of the browser |

        Example:
        | Check Lambda Logs Present | browser_1 |

        Return:
            Boolean (True or False)
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        js_exe = LambdaLocators.get_lambdas_logs
        lambdas_logs = browser.execute_javascript(js_exe)
        if "Server Listening on port 8686!" not in lambdas_logs:
            return False
        return True

    @staticmethod
    def check_no_lambda_logs_present(browser_alias):
        """
        check no lambda logs present
        | browser_alias |  alias of the browser |

        Example:
        | Check No Lambda Logs Present | browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(LambdaLocators.no_lambda_logs_label, timeout=LambdaKeywords.timeout)
