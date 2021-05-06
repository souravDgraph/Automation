# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring
"""
Author: santhosh@dgraph.io
"""

from Slash.keywords.browser.browser_keywords import BrowserKeywords
from Slash.locators.super_admin.super_admin import SuperAdminLocators

__all__ = ['SuperAdminKeywords']
__author__ = "Santhosh S"
__version__ = "1.0"
__maintainer__ = "Santhosh S"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"


class SuperAdminKeywords():
    """ 
    Super Admin Page Keyword Library
    """
    timeout = 10

    @staticmethod
    def validate_search_deployment_fields(browser_alias, search_deployment_fields):
        """
        Validate search deployment fields

        | browser_alias | Alias of the browser |
        | search_deployment_fields | deployment fields to search |

        Example:
            Validate Search Deployment Fields    Browser1    ['User Email', 'Deployment ID', 'Endpoint']
        """       
        browser = BrowserKeywords.switch_browser(browser_alias)
        for each_field in range(len(search_deployment_fields)):
            browser.element_should_be_visible(SuperAdminLocators.list_name.replace("%s", search_deployment_fields[each_field]))
            browser.element_should_be_visible(SuperAdminLocators.search_input_field.replace("%s", search_deployment_fields[each_field]))
            browser.click_element(SuperAdminLocators.list_name.replace("%s", search_deployment_fields[each_field]), timeout=SuperAdminKeywords.timeout)
            if each_field!=len(search_deployment_fields)-1:
                browser.click_element(SuperAdminLocators.list_name.replace("%s", search_deployment_fields[each_field+1]), timeout=SuperAdminKeywords.timeout)
    
    @staticmethod
    def search_deployment(browser_alias, search_type, input_text):
        """
         search deployment 

        | browser_alias | Alias of the browser |
        | search_type | search field for the deployment |
        | input_text | value for the search field |

        Example:
            Validate Search Deployment Fields    Browser1    User Email     santhosh@dgraph.io
        """ 
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.seach_deployment_list_button, timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.list_name.replace("%s", "User Email"), timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.list_name.replace("%s", search_type), timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.list_name.replace("%s", search_type), 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.search_input_field.replace("%s", search_type))
        browser.input_text(SuperAdminLocators.search_input_field.replace("%s", search_type), input_text)
        browser.click_element(SuperAdminLocators.search_btn, timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_response_for_invalid_search(browser_alias, response="No deployments found."):
        """
        Validate response for invalid search

        | browser_alias | Alias of the browser |
        | response | response for the invalid search |

        Example:
            Validate Response For Invalid Search    Browser1 
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.no_deployment_found.replace("%s", response), 
                                                    timeout=SuperAdminKeywords.timeout)
    
    @staticmethod
    def validate_deployment_detail_labels(browser_alias, deployment_labels, backend_name):
        """
        Validate deployment detail labels

        | browser_alias | Alias of the browser |
        | deployment_labels | deployment labels for the backend |
        | backend_name | name of the backend |

        Example:
            Validate Deployment Detail Labels    Browser1    ['Dgraph HA','Do Not Freeze','Deployment Mode']      Test
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.user_info_label,
                                                        timeout=SuperAdminKeywords.timeout)
        for each_deployment_label in deployment_labels:
            browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "ID").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_detail_links(browser_alias, deployment_links, backend_name):
        """
        Validate deployment detail links

        | browser_alias | Alias of the browser |
        | deployment_links | deployment links for the backend |
        | backend_name | name of the backend |

        Example:
            Validate Deployment Detail Links    Browser1    ['Ratel','ChartIO']      Test
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        for each_deployment_link in deployment_links:
            browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", each_deployment_link).replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.edit_btn.replace("%s", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def click_edit_button(browser_alias, backend_name):
        """
        Click edit button on the search deployment page

        | browser_alias | Alias of the browser |
        | backend_name | name of the backend |

        Example:
            Click Edit Button    Browser1       Test
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.edit_btn.replace("%s", backend_name),
                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.edit_deployment_label,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_field_tooltip_message(browser_alias, deployment_field, tooltip_message):
        """
        Validate deployment field tooltip message

        | browser_alias | Alias of the browser |
        | deployment_field | deployment field name |
        | tooltip_message | tooltip message for the backend |

        Example:
           Validate Deployment Field Tooltip Message   Browser1    Deployment Size        Defaults to Small
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_label.replace("%s", deployment_field),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.deployment_field_tooltip.replace("%s", deployment_field))
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_tooltip_message.replace("%s", tooltip_message),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_field_values(browser_alias, deployment_field, values, know_more_link=None):
        """
        Validate deployment field values

        | browser_alias | Alias of the browser |
        | deployment_field | deployment field name |
        | values | values for the deployment field |
        | know_more | know more link for the deployment field | 

        Example:
           Validate Deployment Field Values    Browser1    Do Not Freeze     ['False', 'True']
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.deployment_field_button.replace("%s", deployment_field))
        browser.click_element(SuperAdminLocators.deployment_field_button.replace("%s", deployment_field),
                                                timeout=SuperAdminKeywords.timeout)
        if type(values) is list:
            for each_value in values:
                browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_list_value.replace("%s", deployment_field).replace("value", each_value),
                                                            timeout=SuperAdminKeywords.timeout)
        elif type(values) is str:
            browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_input_value.replace("%s", deployment_field).replace("default_value", values),
                                                            timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.deployment_field_button.replace("%s", deployment_field),
                                                timeout=SuperAdminKeywords.timeout)
        if know_more_link:
            browser.click_element(SuperAdminLocators.know_more_link.replace("%s", know_more_link), timeout=SuperAdminKeywords.timeout)
            browser.go_back()

    @staticmethod
    def validate_fields_alert_message(browser_alias, deployment_fields):
        """
        Validate fields alert message

        | browser_alias | Alias of the browser |
        | deployment_fields | deployment fields name |

        Example:
           Validate Fields Alert Message    Browser1    ['Deployment Size', 'Deployment Mode']
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        for each_deployment_field in deployment_fields:
            browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", each_deployment_field),
                                                        timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def check_default_value_present_for_fields(browser_alias, deployment_fields_values_dict, backend_name):
        """
        Check default value present for fields

        | browser_alias | Alias of the browser |
        | deployment_fields_values_dict | deployment fields name with default value |
        | backend_name | name of the backend |

        Example:
           Check Default Value Present For Fields    Browser1    {'Do Not Freeze': 'False', 'Deployment Mode':'Free'}     Test
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_name_field.replace("%s", backend_name), 
                                                    timeout=SuperAdminKeywords.timeout)
        for deployment_field, deployment_value in deployment_fields_values_dict.items():
            if deployment_value and deployment_field not in ['Backup Interval', 'Backup Bucket Format', 'Dgraph Lambda Script']:
                browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_value.replace("%s", deployment_field).replace("value", deployment_value), 
                                                            timeout=SuperAdminKeywords.timeout)
            else:
                browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_input_value.replace("%s", deployment_field).replace("default_value", deployment_value), 
                                                            timeout=SuperAdminKeywords.timeout)
            browser.wait_until_page_contains_element(SuperAdminLocators.deployment_field_button.replace("%s", deployment_field),
                                                            timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_button,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_button,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.update_button,
                                                    timeout=SuperAdminKeywords.timeout)
                     
    @staticmethod
    def click_back_button(browser_alias):
        """
        Click the back button on the edit deploymen page

        | browser_alias | Alias of the browser |

        Example:
           Click Back Button    Browser1   
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.back_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.search_deployment_label, 
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def change_deployment_field_value(browser_alias, deployment_field_name, old_value, new_value):
        """
        Change the deployment field value 

        | browser_alias | Alias of the browser |
        | deployment_field_name | name of the deployment field |
        | old_value | old value for the field |
        | new_value | new value for the field |

        Example:
           Change Deployment Field Value    Browser1    Do Not Freeze    False     True
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.deployment_field_button.replace("%s", deployment_field_name))
        browser.click_element(SuperAdminLocators.deployment_field_button.replace("%s", deployment_field_name), 
                                                timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.deployment_field_list_value.replace("%s", deployment_field_name).replace("value", new_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.deployment_field_value.replace("%s", deployment_field_name).replace("value", new_value))


    @staticmethod
    def click_update_button(browser_alias):
        """
        Click update button in the edit deployment page

        | browser_alias | Alias of the browser |

        Example:
           Click Update Button    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.update_button)
        browser.click_element(SuperAdminLocators.update_button, timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def check_deployment_field_value(browser_alias, deployment_field, value):
        """
        Check the deployment field value 

        | browser_alias | Alias of the browser |
        | deployment_field_name | name of the deployment field |
        | value | value for the field |

        Example:
           Check Deployment Field Value    Browser1    Do Not Freeze    False
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.deployment_field_value.replace("%s", deployment_field).replace("value", value))
        
    @staticmethod
    def click_protect_button(browser_alias):
        """
        Click protect button in the edit deployment page

        | browser_alias | Alias of the browser |

        Example:
           Click Protect Button    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.protect_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.unprotect_button,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def check_unprotect_button_present(browser_alias):
        """
        Check unprotect button present in the edit deployment page

        | browser_alias | Alias of the browser |

        Example:
           Check Unprotect Button Present    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.unprotect_button,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def click_update_button_for_protect_deployment(browser_alias):
        """
        Click update button for protect deployment in the edit deployment page

        | browser_alias | Alias of the browser |

        Example:
           Click Update Button For Protect Deployment    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.update_button, timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def click_unprotect_button(browser_alias):
        """
        Click unprotect button in the edit deployment page

        | browser_alias | Alias of the browser |

        Example:
           Click Unprotect Button    Browser1
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.unprotect_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_button,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_alert(browser_alias, alert_message):
        """
        Validate alert message

        | browser_alias | Alias of the browser |
        | alert_message | alert message |

        Example:
           Validate Alert    Browser1       Deployment has been updated
           Validate Alert    Browser1       Something went wrong
        """
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.alert_message.replace("%s", alert_message),
                                                            timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SuperAdminLocators.alert_message.replace("%s", alert_message),
                                                            timeout=SuperAdminKeywords.timeout)
