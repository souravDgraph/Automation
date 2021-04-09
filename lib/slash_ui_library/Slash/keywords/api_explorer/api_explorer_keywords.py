# !/usr/bin/env python
# coding=utf-8
# pylint: disable=missing-function-docstring
"""
Author: santhosh@dgraph.io
"""

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
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(ApiExplorerLocators.dropdown_list, timeout=ApiExplorerKeywords.timeout)
        browser.select_from_list_by_value(ApiExplorerLocators.dropdown_list, query_type)

    @staticmethod
    def click_add_query_type_button(browser_alias, query_type):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.add_button, timeout=ApiExplorerKeywords.timeout)
        browser.wait_until_page_contains_element(ApiExplorerLocators.query_label.replace("%s", query_type), timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def expand_add_query(browser_alias, process, type_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.add_mutation_span.replace("%s", process+type_name), timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def add_value_to_field(browser_alias, field_name, field_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.field_checkbox.replace("%s", field_name), timeout=ApiExplorerKeywords.timeout)
        browser.input_text(ApiExplorerLocators.field_input_textbox.replace("%s", field_name), field_value)

    @staticmethod
    def click_execute_query_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(ApiExplorerLocators.execute_query_button, timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def click_remove_query_button(browser_alias, query_type):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.mouse_over(ApiExplorerLocators.query_label.replace("%s", query_type))
        browser.click_element(ApiExplorerLocators.remove_query_button.replace("%s", query_type), timeout=ApiExplorerKeywords.timeout)

    @staticmethod
    def select_search_fields(browser_alias, search_fields):
        browser = BrowserKeywords.switch_browser(browser_alias)
        for each_field in search_fields:
            browser.click_element(ApiExplorerLocators.field_checkbox.replace("%s", each_field), timeout=ApiExplorerKeywords.timeout)
