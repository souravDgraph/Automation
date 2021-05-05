# !/usr/bin/env python
# coding=utf-8
# pylint: disable=missing-function-docstring
"""
Author: vivetha@dgraph.io
"""

from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.organization.organization import OrganizationLocators
from robot.api import logger

__all__ = ['OrganizationKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class OrganizationKeywords():
    """Dashboard/Landing Page Keyword Library.

    Main operations:

    - create Organization.
    """
    timeout = 10

    @staticmethod
    def get_organization_list(browser_alias):

        headers = ["NAME", "OWNER"]
        browser = BrowserKeywords.switch_browser(browser_alias)
        org_header = browser.get_text(OrganizationLocators.org_list_headers)
        ui_headers = org_header.split("\n")
        org_list = browser.get_text(OrganizationLocators.org_list)
        if ui_headers.sort() != headers.sort():
            raise Exception("Expected table headers not found")
        logger.info("Headers %s" % str(ui_headers))
        logger.info(org_list)

    @staticmethod
    def click_organization(browser_alias, organization):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(OrganizationLocators.org.replace("%s", organization))

    @staticmethod
    def click_add_member(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(OrganizationLocators.add_member)

    @staticmethod
    def fill_org_member_email(browser_alias, email):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.input_text(OrganizationLocators.org_email, email)

    @staticmethod
    def click_add_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(OrganizationLocators.add_button)

    @staticmethod
    def add_member_to_organization(browser_alias, organization):
        OrganizationKeywords.click_add_member(browser_alias)
        OrganizationKeywords.fill_org_member_email(browser_alias, organization)
        OrganizationKeywords.click_add_button(browser_alias)

    @staticmethod
    def remove_member_from_organization(browser_alias, organization):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(OrganizationLocators.remove_org.replace("%s", organization))

    @staticmethod
    def leave_member_from_organization(browser_alias, organization):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(OrganizationLocators.leave_org.replace("%s", organization))

    @staticmethod
    def validate_organization_alert_and_close_dialogue(browser_alias, expected_data):
        browser = BrowserKeywords.switch_browser(browser_alias)
        alert_text = browser.get_text(OrganizationLocators.add_member_alert)
        logger.info("Expected Alert : %s" % expected_data)
        logger.info("Actual Alert : %s" % alert_text)
        if expected_data not in alert_text:
            raise Exception("Expected alert is not found")

    @staticmethod
    def click_create_organization_button(browser_alias):
        """
        click create organization button
        | browser_alias |  alias of the browser |

        Example:
        | Click Create Organization Button | Browser_1 |
        
        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(OrganizationLocators.create_org_button, timeout=OrganizationKeywords.timeout)
        browser.wait_until_page_contains_element(OrganizationLocators.create_new_org_label, timeout=OrganizationKeywords.timeout)

    @staticmethod
    def add_organization(browser_alias, org_name):
        """
        add an organization
        | browser_alias |  alias of the browser |
        | org_name | name of the organization |

        Example:
        | Add Organization | Browser_1 | Labs |
        
        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.input_text(OrganizationLocators.organization_textbox, org_name)
        browser.click_element(OrganizationLocators.create_button, timeout=OrganizationKeywords.timeout)
        browser.wait_until_page_contains_element(OrganizationLocators.org.replace("%s", org_name), timeout=OrganizationKeywords.timeout)
