# !/usr/bin/env python
# coding=utf-8
# pylint: disable=missing-function-docstring
"""
Author: vivetha@dgraph.io
"""

import time
from Slash.keywords.settings.constants import CLONE_TEXT, DELETE_TEXT
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.settings.settings import SettingsLocators
from robot.api import logger

__all__ = ['SettingsKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class SettingsKeywords:
    """Login Page Keyword Library.

    Main operations:

    - Login and Logout page related operations
    """
    timeout = 10

    @staticmethod
    def validate_general_tab_data(browser_alias, backend_name, organization):
        browser = BrowserKeywords.switch_browser(browser_alias)
        ui_backend_name = browser.get_value(SettingsLocators.backend_name,
                                            timeout=SettingsKeywords.timeout)
        logger.info(ui_backend_name)
        logger.info(backend_name)
        if ui_backend_name.strip() != backend_name.strip():
            raise Exception("Expected backend Name Not found")

        ui_organization = browser.get_text(SettingsLocators.organization_name,
                                           timeout=SettingsKeywords.timeout)
        logger.info(ui_organization)
        logger.info(organization)
        if ui_organization != organization:
            raise Exception("Expected Organization Name Not found")
        browser.page_should_contain_element(SettingsLocators.clone_backend)
        browser.page_should_contain_element(SettingsLocators.delete_backend)
        ui_clone_text = browser.get_text(CLONE_TEXT)
        logger.info(ui_clone_text)
        logger.info(CLONE_TEXT)
        if CLONE_TEXT not in ui_clone_text:
            raise Exception("Expected clone text Not found")

        ui_delete_text = browser.get_text(DELETE_TEXT)
        logger.info(ui_delete_text)
        logger.info(DELETE_TEXT)
        if DELETE_TEXT not in ui_delete_text:
            raise Exception("Expected Delete text Not found")

    @staticmethod
    def delete_deployment(browser_alias,
                          backend_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.delete_backend,
                              timeout=SettingsKeywords.timeout)
        browser.input_text(SettingsLocators.delete_conformation_input_field,
                           backend_name,
                           timeout=SettingsKeywords.timeout)
        time.sleep(10)
        browser.click_element(SettingsLocators.destroy_button,
                              timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.destroy_button,
                              timeout=SettingsKeywords.timeout)

    @staticmethod
    def update_backend_organization(browser_alias, organization):
        browser = BrowserKeywords.switch_browser(browser_alias)
        ui_organization = browser.get_text(SettingsLocators.organization_name,
                                           timeout=SettingsKeywords.timeout)
        browser.page_should_not_contain_element(SettingsLocators.update_button)
        if ui_organization != organization:
            browser.click_element(SettingsLocators.organization_select,
                                  timeout=SettingsKeywords.timeout)
            browser.click_element(SettingsLocators.organization.replace("%s", organization),
                                  timeout=SettingsKeywords.timeout)
            browser.click_element(SettingsLocators.update_button,
                                  timeout=SettingsKeywords.timeout)

    @staticmethod
    def click_api_key_tab(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.api_keys_tab, timeout=SettingsKeywords.timeout)

    @staticmethod
    def create_new_api_key(browser_alias, api_key_name, key_type=None):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.create_api_key_button, timeout=SettingsKeywords.timeout)
        browser.input_text(SettingsLocators.enter_api_name_textbox,
                           api_key_name,
                           timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.create_api_button, timeout=SettingsKeywords.timeout)

    @staticmethod
    def click_general_tab(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.general_tab, timeout=SettingsKeywords.timeout)

    @staticmethod
    def verify_api_key_generated(browser_alias, api_key_name): 
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SettingsLocators.okay_button, timeout=timeout.SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.okay_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.api.replace("%s", api_key_name), timeout=SettingsKeywords.timeout)

    @staticmethod
    def delete_api_key(browser_alias, api_key_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.delete_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.delete_api_key_confirm, timeout=timeout.SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.delete_api_key_confirm, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SettingsLocators.api.replace("%s", api_key_name), timeout=SettingsKeywords.timeout)
