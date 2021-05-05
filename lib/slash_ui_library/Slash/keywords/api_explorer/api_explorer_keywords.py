# !/usr/bin/env python
# coding=utf-8
# pylint: disable=missing-function-docstring
"""
Author: santhosh@dgraph.io
"""
import re, json, time
from robot.api import logger
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.api_explorer.api_explorer import ApiExplorerLocators

__all__ = ['ApiExplorerKeywords']
__author__ = "Santhosh S"
__version__ = "1.0"
__maintainer__ = "Santhosh S"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"

class ApiExplorerKeywords():
    """
    API Explorer Keywords
    """
    timeout = 10

    @staticmethod
    def select_query_type(browser_alias, query_type):
        """
        select query type
        | browser_alias |  alias of the browser |
        | query_type | query type to perform  |

        Example:
        | Select Query Type | Browser_1 | mutation |
        | Select Query Type | Browser_1 | query |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(ApiExplorerLocators.dropdown_list, timeout=ApiExplorerKeywords.timeout)
        browser.select_from_list_by_value(ApiExplorerLocators.dropdown_list, query_type)

    @staticmethod
    def click_add_query_type_button(browser_alias, query_type):
        """
        click add query type button
        | browser_alias |  alias of the browser |
        | query_type | query type to perform  |

        Example:
        | Click Add Query Type Button | Browser_1 | mutation |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.add_button, timeout=ApiExplorerKeywords.timeout)
        browser.wait_until_page_contains_element(ApiExplorerLocators.query_label.replace("%s", query_type), timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def expand_add_query(browser_alias, process, type_name):
        """
        expand add query button
        | browser_alias |  alias of the browser |
        | process | name of the process |
        | type_name | name of the type  |

        Example:
        | Expand Add Query | Browser_1 | add | User |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.add_mutation_span.replace("%s", process+type_name), timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def add_value_to_field(browser_alias, field_name, field_value):
        """
        add value to field
        | browser_alias |  alias of the browser |
        | field_name | name of the field |
        | field_value | value for the field  |

        Example:
        | Add Value To Field | Browser_1 | name | user1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.field_checkbox.replace("%s", field_name), timeout=ApiExplorerKeywords.timeout)
        browser.input_text(ApiExplorerLocators.field_input_textbox.replace("%s", field_name), field_value)

    @staticmethod
    def click_execute_query_button(browser_alias):
        """
        click execute query button
        | browser_alias |  alias of the browser |

        Example:
        | Click Execute Query Button | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.execute_query_button, timeout=ApiExplorerKeywords.timeout)
    
    @staticmethod
    def get_query_result(browser_alias):
        """
        get the query result
        | browser_alias |  alias of the browser |

        Example:
        | Get Query Result | Browser_1 |

        Return:
            { queryUser : [{ id: 0xa }] }
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        time.sleep(5)
        height = browser.execute_javascript(ApiExplorerLocators.get_scroll_height)
        browser.execute_javascript(ApiExplorerLocators.set_scroll_top.replace("%s", str(height)))
        js_exe = ApiExplorerLocators.get_query_data
        response = browser.execute_javascript(js_exe)
        logger.info(response)
        response = re.sub('\xa0', '', response) 
        response = json.loads(response)
        logger.info(response['data'])
        return response['data']

    @staticmethod
    def click_remove_query_button(browser_alias, query_type):
        """
        click remove query button
        | browser_alias |  alias of the browser |
        | query_type | type of the query to be removed |

        Example:
        | Click Remove Query Button | Browser_1 | query |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.mouse_over(ApiExplorerLocators.query_label.replace("%s", query_type))
        browser.click_element(ApiExplorerLocators.remove_query_button.replace("%s", query_type), timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def select_search_fields(browser_alias, search_fields):
        """
        select all the fields be to searched
        | browser_alias |  alias of the browser |
        | search_fields | search fields |

        Example:
        | Select Search Fields | Browser_1 | ["name", "age", "id" ] |
        
        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        for each_field in search_fields:
            browser.click_element(ApiExplorerLocators.field_checkbox.replace("%s", each_field), timeout=ApiExplorerKeywords.timeout)