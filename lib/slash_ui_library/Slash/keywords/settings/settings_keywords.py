# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.settings.settings import SettingsLocators
from Slash.keywords.settings.constants import clone_text, delete_text
import time
# pylint: disable=too-many-arguments


__all__ = ['SettingsKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class SettingsKeywords(object):
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
        ui_clone_text = browser.get_text(SettingsLocators.clone_text)
        logger.info(ui_clone_text)
        logger.info(clone_text)
        if clone_text not in ui_clone_text:
            raise Exception("Expected clone text Not found")

        ui_delete_text = browser.get_text(SettingsLocators.delete_text)
        logger.info(ui_delete_text)
        logger.info(delete_text)
        if delete_text not in ui_delete_text:
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
        time.sleep(5)
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




















