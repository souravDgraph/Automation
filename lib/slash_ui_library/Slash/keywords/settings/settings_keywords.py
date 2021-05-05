# !/usr/bin/env python
# coding=utf-8
# pylint: disable=missing-function-docstring
"""
Author: vivetha@dgraph.io
"""

import time
from robot.api.deco import keyword
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
        """
        delete the backend and wait for the confirmation message.
        | browser_alias |  alias of the browser |
        | backend_name |  name of the backend |

        Example:
        | Delete Deployment | Browser_1 | test |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.delete_backend,
                              timeout=SettingsKeywords.timeout)
        browser.input_text(SettingsLocators.delete_conformation_input_field,
                           backend_name,
                           timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.destroy_button,
                              timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.delete_confirm_message, 
                                            timeout=SettingsKeywords.timeout)

    @staticmethod
    def check_deployment_is_deleted(browser_alias, backend_name):
        """
        check the deployment is deleted.
        | browser_alias |  alias of the browser |
        | backend_name |  name of the backend |

        Example:
        | Check Deployment Is Deleted | Browser_1 | test |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_does_not_contain_element(SettingsLocators.backend_dropdown_list.replace("%s", backend_name), 
                                                    timeout=SettingsKeywords.timeout)

    @staticmethod
    def update_backend_organization(browser_alias, new_org_name, current_org_name=None):
        """
        update the organization name for the backend.
        | browser_alias |  alias of the browser |
        | old_organization | organization name present already (optional) |
        | organization |  name of the organization |

        Example:
        | Update Backend Organization | Browser_1 | test | Labs |
        | Update Backend Organization | Browser_1 | Labs | 

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        if(current_org_name):
            browser.click_element(SettingsLocators.organization_name_button.replace("%s", current_org_name), timeout=SettingsKeywords.timeout)
        else:
            browser.click_element(SettingsLocators.organization_name_button.replace("%s", "Select organization"), timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.organization_name_list.replace("%s", new_org_name), timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.update_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.organization_name_button.replace("%s",new_org_name), timeout=SettingsKeywords.timeout)

    @staticmethod
    def remove_backend_organization(browser_alias):
        """
        remove the backend organization.
        | browser_alias |  alias of the browser |

        Example:
        | Remove Backend Organization | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.remove_org_button, timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.remove_org_popup_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.organization_name_button.replace("%s", "Select organization"), timeout=SettingsKeywords.timeout)

    @staticmethod
    def click_api_key_tab(browser_alias):
        """
        click the api key tab for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click Api Key Tab | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.api_keys_tab, timeout=SettingsKeywords.timeout)

    @staticmethod
    def create_new_api_key(browser_alias, api_key_name, key_type=None):
        """
        create a new api key for the backend.
        | browser_alias |  alias of the browser |
        | api_key_name | name of the api key |
        | key_type | type of api key |

        Example:
        | Create New Api Key | Browser_1 | test_api | 

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.create_api_key_button, timeout=SettingsKeywords.timeout)
        browser.input_text(SettingsLocators.enter_api_name_textbox,
                           api_key_name,
                           timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.create_api_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.okay_button, timeout=SettingsKeywords.timeout)

    @staticmethod
    def click_general_tab(browser_alias):
        """
        click the general tab for the backend.
        | browser_alias |  alias of the browser |

        Example:
        | Click General Tab | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.general_tab, timeout=SettingsKeywords.timeout)

    @staticmethod
    def verify_api_key_generated(browser_alias, api_key_name):
        """
        verify the api key generated for the backend.
        | browser_alias |  alias of the browser |
        | api_key_name | name of the api key |

        Example:
        | Verify Api Key Generated | Browser_1 | test_api |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SettingsLocators.okay_button, timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.okay_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.api.replace("%s", api_key_name), timeout=SettingsKeywords.timeout)

    @staticmethod
    def delete_api_key(browser_alias, api_key_name):
        """
        delete the api key for the backend.
        | browser_alias |  alias of the browser |
        | api_key_name | name of the api key |

        Example:
        | Delete Api Key | Browser_1 | test_api |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.delete_button, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.delete_api_key_confirm, timeout=SettingsKeywords.timeout)
        browser.click_element(SettingsLocators.delete_api_key_confirm, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SettingsLocators.api.replace("%s", api_key_name), timeout=SettingsKeywords.timeout)

    @staticmethod
    def click_clone_backend(browser_alias):
        """
        click the clone backend button
        | browser_alias |  alias of the browser |

        Example:
        | Click Clone Backend | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SettingsLocators.clone_backend, timeout=SettingsKeywords.timeout)
        browser.wait_until_page_contains_element(SettingsLocators.clone_deployment_label, timeout=SettingsKeywords.timeout)
