# !/usr/bin/env python
# coding=utf-8
# pylint: disable=missing-function-docstring
"""
Author: santhosh@dgraph.io
"""

import re
from robot.api import logger
from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.schema.schema import SchemaLocators
from selenium.webdriver.common.keys import Keys

__all__ = ['SchemaKeywords']
__author__ = "Santhosh S"
__version__ = "1.0"
__maintainer__ = "Santhosh S"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"


class SchemaKeywords:
    """
    Schema Page Keyword Library
    """
    timeout = 10

    @staticmethod
    def click_switch_to_ui_mode(browser_alias):
        """
        click switch to ui mode button
        | browser_alias |  alias of the browser |

        Example:
        | Click Switch To Ui Mode | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.ui_mode_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_contains_element(SchemaLocators.inspect_panel_label,
                                                    timeout=SchemaKeywords.timeout)

    @staticmethod
    def click_switch_to_text_mode(browser_alias):
        """
        click switch to text mode button
        | browser_alias |  alias of the browser |

        Example:
        | Click Switch To Text Mode | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.text_mode_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_contains_element(SchemaLocators.ui_mode_button,
                                                    timeout=SchemaKeywords.timeout)
    
    @staticmethod
    def deploy_schema(browser_alias):
        """
        click deploy schema button
        | browser_alias |  alias of the browser |

        Example:
        | Deploy Schema | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.deploy_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_element_is_visible(SchemaLocators.okay_button, timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.okay_button, timeout=SchemaKeywords.timeout)

    @staticmethod
    def add_type(browser_alias):
        """
        click add type button
        | browser_alias |  alias of the browser |

        Example:
        | Add Type | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.add_button, timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.add_type_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_contains_element(SchemaLocators.default_type_name.replace("%s", "UntitledType0"), timeout=SchemaKeywords.timeout)

    @staticmethod
    def change_type_name(browser_alias, old_type_name, new_type_name):
        """
        change type name
        | browser_alias |  alias of the browser |
        | old_type_name | old name of the type |
        | new_type_name | new name for the type |

        Example:
        | Change Type Name | Browser_1 | UntitledType0 | User |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.edit_button.replace("%s", old_type_name), timeout=SchemaKeywords.timeout)
        browser.get_webelement(SchemaLocators.editable_type_name.replace("%s", old_type_name)).send_keys(Keys.COMMAND, 'a')
        browser.get_webelement(SchemaLocators.editable_type_name.replace("%s", old_type_name)).send_keys(new_type_name)
        browser.click_element(SchemaLocators.save_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_contains_element(SchemaLocators.default_type_name.replace("%s", new_type_name), timeout=SchemaKeywords.timeout)

    @staticmethod
    def get_deployed_schema(browser_alias):
        """
        get the deployment schema
        | browser_alias |  alias of the browser |

        Example:
        | Get Deployed Schema | Browser_1 |

        Return:
            Schema
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        js_exe = "return document.getElementsByClassName('CodeMirror-code').valueOf()[0].textContent"
        schema = browser.execute_javascript(js_exe)
        schema = re.sub('[1-9,\u200b]', '', schema)
        logger.info(schema)
        return schema

    @staticmethod
    def add_field(browser_alias, type_name):
        """
        click add field button
        | browser_alias |  alias of the browser |
        | type_name | type name for which the field to be added |

        Example:
        | Add Field | Browser_1 | User |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.add_field_button.replace("%s", type_name), timeout=SchemaKeywords.timeout)

    @staticmethod
    def change_field_name(browser_alias, type_name, old_field_name, new_field_name):
        """
        change field name
        | browser_alias |  alias of the browser |
        | type_name | type name for which the field to be added |
        | old_field_name | current name of the field |
        | new_field_name | new name for the field |

        Example:
        | Change Field Name | Browser_1 | User | untitledfield | age |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.input_text(SchemaLocators.editable_field_name.replace("%s", type_name).replace("old_field_name", old_field_name), new_field_name)

    @staticmethod
    def change_field_type(browser_alias, type_name, field_name, old_data_type, new_data_type):
        """
        change field name
        | browser_alias |  alias of the browser |
        | type_name | type name for which the field to be added |
        | field_name | name of the field |
        | old_data_type | current data type of the field |
        | new_data_type | data type of the field |

        Example:
        | Change Field Type | Browser_1 | User | untitledfield | age | String | Int

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.field_type_button.replace("%s", type_name).replace("old_data_type", old_data_type), 
                                timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.select_field_type.replace("%s", type_name).replace("field_name", field_name).replace("new_data_type", new_data_type), 
                                timeout=SchemaKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SchemaLocators.field_type_button.replace("%s", type_name).replace("field_name", field_name).replace("old_data_type", old_data_type), 
                                timeout=SchemaKeywords.timeout)

    @staticmethod
    def select_unused_field(browser_alias, field_name):
        """
        change field name
        | browser_alias |  alias of the browser |
        | field_name | name of the field |

        Example:
        | Select Unused Field | Browser_1 | User.age |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.unused_fields.replace("%s", field_name),
                                timeout=SchemaKeywords.timeout)

    @staticmethod
    def click_drop_button(browser_alias):
        """
        click drop button
        | browser_alias |  alias of the browser |

        Example:
        | Click Drop Button | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.drop_button, timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.success_drop_field_okay_button, timeout=SchemaKeywords.timeout)


    @staticmethod
    def check_dropped_field_is_not_visible(browser_alias, field_name):
        """
        check dropped field is removed from the user interface
        | browser_alias |  alias of the browser |
        | field_name | name of the field |

        Example:
        | Check Dropped Field Is Not Visible | Browser_1 | User.age |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.drop_data_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SchemaLocators.unused_fields.replace("%s", field_name), 
                                                            timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.drop_data_cancel_button, timeout=SchemaKeywords.timeout)

    @staticmethod
    def click_drop_data_button(browser_alias):
        """
        click drop data button
        | browser_alias |  alias of the browser |

        Example:
        | Click Drop Data Button | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.drop_data_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_contains_element(SchemaLocators.drop_data_label, timeout=SchemaKeywords.timeout)

    @staticmethod
    def click_drop_all_data_button(browser_alias):
        """
        click drop all data button
        | browser_alias |  alias of the browser |

        Example:
        | Click Drop All Data Button | Browser_1 |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.drop_all_data_button, timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.drop_all_data_button, timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.success_okay_button, timeout=SchemaKeywords.timeout)

    @staticmethod
    def remove_field(browser_alias, type_name, field_name):
        """
        remove field for the type
        | browser_alias |  alias of the browser |
        | type_name | type name for which the field to be added |
        | field_name | name of the field |

        Example:
        | Remove Field | Browser_1 | User | age |

        Return:
            None
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SchemaLocators.editable_field_name.replace("%s", type_name).replace("old_field_name", field_name), timeout=SchemaKeywords.timeout)
        browser.click_element(SchemaLocators.remove_field_button, timeout=SchemaKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SchemaLocators.editable_field_name.replace("%s", type_name).replace("old_field_name", field_name), 
                                                            timeout=SchemaKeywords.timeout)
                                                            