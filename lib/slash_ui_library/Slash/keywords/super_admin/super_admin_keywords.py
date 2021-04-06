# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring
"""
Author: santhosh@dgraph.io
"""

from robot.api.deco import keyword
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
    def validate_search_deployment_fields(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.list_name.replace("%s", "User Email"))
        browser.element_should_be_visible(SuperAdminLocators.search_input_field.replace("%s", "User Email"))
        browser.click_element(SuperAdminLocators.list_name.replace("%s", "User Email"), timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.list_name.replace("%s", "Deployment ID"), timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.list_name.replace("%s", "Deployment ID"))
        browser.element_should_be_visible(SuperAdminLocators.search_input_field.replace("%s", "Deployment ID"))
        browser.click_element(SuperAdminLocators.list_name.replace("%s", "Deployment ID"), timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.list_name.replace("%s", "Endpoint"), timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.list_name.replace("%s", "Endpoint"))
        browser.element_should_be_visible(SuperAdminLocators.search_input_field.replace("%s", "Endpoint"))

    @staticmethod
    def search_deployment(browser_alias, search_type, input_text):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.list_name.replace("%s", "User Email"), timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.list_name.replace("%s", search_type), timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.list_name.replace("%s", search_type), 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.search_input_field.replace("%s", search_type))
        browser.input_text(SuperAdminLocators.search_input_field.replace("%s", search_type), input_text)
        browser.click_element(SuperAdminLocators.search_btn, timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_response_for_invalid_search(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.no_deployment_found, 
                                                    timeout=SuperAdminKeywords.timeout)
    
    @staticmethod
    def validate_deployment_detail_labels(browser_alias, backend_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.user_info_label,
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "ID").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "Name").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "URL").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "Owner").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "JWT Token").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "Debug Links").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_label.replace("%s", "Configs").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_detail_links(browser_alias, backend_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Grafana HTTP").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Grafana GRPC").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Jaeger").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Ratel").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Alpha Logs").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Zero Logs").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "Kube Events").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_link.replace("%s", "ChartIO").replace("backend", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.edit_btn.replace("%s", backend_name), 
                                                        timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def click_edit_button(browser_alias, backend_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.edit_btn.replace("%s", backend_name),
                                        timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.edit_btn.replace("%s", backend_name),
                                        timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.edit_deployment_label,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_dgraph_lambda_script_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_lambda_script_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.dgraph_lambda_script_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_lambda_script_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_do_not_freeze_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.do_not_freeze_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.do_not_freeze_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.do_not_freeze_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_do_not_freeze_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.do_not_freeze_value.replace("%s", 'False'))
        browser.click_element(SuperAdminLocators.do_not_freeze_value.replace("%s", 'False'), 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.do_not_freeze_list_value.replace("%s", 'False'),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.do_not_freeze_list_value.replace("%s", 'True'),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_dgraph_ha_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_ha_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.dgraph_ha_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_ha_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_dgraph_ha_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.dgraph_ha_default_value.replace("%s", 'False'))
        browser.click_element(SuperAdminLocators.dgraph_ha_default_value.replace("%s", 'False'), 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_ha_value.replace("%s", 'False'),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_ha_value.replace("%s", 'True'),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_mode_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_mode_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.deployment_mode_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_mode_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_mode_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.deployment_mode_link, timeout=SuperAdminKeywords.timeout)
        browser.go_back()
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_mode_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.deployment_mode_graphql_value)
        browser.click_element(SuperAdminLocators.deployment_mode_graphql_value, 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_mode_value.replace("%s", 'Flexible'),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_mode_value.replace("%s", 'Read Only'),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_size_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_size_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.deployment_size_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_size_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_deployment_size_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.deployment_size_link, timeout=SuperAdminKeywords.timeout)
        browser.go_back()
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_size_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.deployment_size_small_value)
        browser.click_element(SuperAdminLocators.deployment_size_small_value, 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_size_value.replace("%s", 'Medium (2C)'),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_size_value.replace("%s", 'Large (4C)'),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_backup_interval_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_interval_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.backup_interval_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_interval_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_backup_interval_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.backup_interval_default_value)
        browser.click_element(SuperAdminLocators.backup_interval_link, timeout=SuperAdminKeywords.timeout)
        browser.go_back()

    @staticmethod
    def validate_backup_bucket_format_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_bucket_format_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.backup_bucket_format_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_bucket_format_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_backup_bucket_format_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.backup_bucket_format_default_value)
        browser.click_element(SuperAdminLocators.backup_bucket_format_link, timeout=SuperAdminKeywords.timeout)
        browser.go_back()

    @staticmethod
    def validate_jaeger_tracing_field_tooltip_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.jaeger_tracing_label,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.mouse_over(SuperAdminLocators.jaeger_tracing_tooltip)
        browser.wait_until_page_contains_element(SuperAdminLocators.jaeger_tracing_tooltip_message,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_jaeger_tracing_field_values(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.jaeger_tracing_default_value)
        browser.click_element(SuperAdminLocators.jaeger_tracing_default_value, 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.jaeger_tracing_list_value.replace("%s", 'False'),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.jaeger_tracing_list_value.replace("%s", 'True'),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def validate_fields_alert_message(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Do Not Freeze"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Enable ACL"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Dgraph HA"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Deployment Mode"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Deployment Size"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Backup Interval"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Backup Bucket Format"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Enable Jaeger Tracing"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Jaeger Trace Ratio"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Jaeger Size"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Deployment Type"),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.fields_alert_message.replace("%s", "Dgraph Lambda Script"),
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def check_default_value_present_for_fields(browser_alias, backend_name):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_name_field.replace("%s", backend_name), 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.do_not_freeze_value.replace("%s", 'False'), 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_ha_default_value.replace("%s", 'False'), 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_mode_graphql_value, 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_size_small_value, 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.jaeger_tracing_default_value, 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_interval_default_value, 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_bucket_format_default_value, 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.enable_acl_default_value, 
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_lambda_script_default_value,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.deployment_type_default_value,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_button,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.backup_button,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.update_button,
                                                    timeout=SuperAdminKeywords.timeout)

                                                
    @staticmethod
    def click_back_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.back_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.search_deployment_label, 
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def change_do_not_freeze_field(browser_alias, current_freeze_value, new_freeze_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.do_not_freeze_value.replace("%s", current_freeze_value))
        browser.click_element(SuperAdminLocators.do_not_freeze_value.replace("%s", current_freeze_value), 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.do_not_freeze_list_value.replace("%s", new_freeze_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.do_not_freeze_list_value.replace("%s", new_freeze_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.do_not_freeze_value.replace("%s", new_freeze_value))

    @staticmethod
    def change_jaeger_tracing_field(browser_alias, jaeger_tracing_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.jaeger_tracing_default_value)
        browser.click_element(SuperAdminLocators.jaeger_tracing_default_value, 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.jaeger_tracing_list_value.replace("%s", jaeger_tracing_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.jaeger_tracing_list_value.replace("%s", jaeger_tracing_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.jaeger_tracing_value.replace("%s", jaeger_tracing_value))

    @staticmethod
    def change_dgraph_ha_field(browser_alias, current_dgraph_ha_value, new_dgraph_ha_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.dgraph_ha_default_value.replace("%s", current_dgraph_ha_value))
        browser.click_element(SuperAdminLocators.dgraph_ha_default_value.replace("%s", current_dgraph_ha_value), 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.dgraph_ha_value.replace("%s", new_dgraph_ha_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.click_element(SuperAdminLocators.dgraph_ha_value.replace("%s", new_dgraph_ha_value),
                                                    timeout=SuperAdminKeywords.timeout)
        browser.element_should_be_visible(SuperAdminLocators.dgraph_ha_default_value.replace("%s", new_dgraph_ha_value))

    @staticmethod
    def click_update_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.update_button)
        browser.click_element(SuperAdminLocators.update_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.update_alert_message, 
                                                timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SuperAdminLocators.update_alert_message, 
                                                            timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def check_do_not_freeze_value(browser_alias, freeze_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.do_not_freeze_value.replace("%s", freeze_value))

    @staticmethod
    def check_jaeger_tracing_value(browser_alias, jaeger_tracing_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.jaeger_tracing_value.replace("%s", jaeger_tracing_value))

    @staticmethod
    def check_dgraph_ha_value(browser_alias, dgraph_ha_value):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.element_should_be_visible(SuperAdminLocators.dgraph_ha_default_value.replace("%s", dgraph_ha_value))

    @staticmethod
    def click_protect_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.protect_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_alert_message,
                                                            timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SuperAdminLocators.protect_alert_message,
                                                            timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.unprotect_button,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def check_unprotect_button_present(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.wait_until_page_contains_element(SuperAdminLocators.unprotect_button,
                                                    timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def click_update_button_for_protect_deployment(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.update_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_update_alert_message,
                                                    timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SuperAdminLocators.protect_update_alert_message,
                                                            timeout=SuperAdminKeywords.timeout)

    @staticmethod
    def click_unprotect_button(browser_alias):
        browser = BrowserKeywords.switch_browser(browser_alias)
        browser.click_element(SuperAdminLocators.unprotect_button, timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_alert_message,
                                                            timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_does_not_contain_element(SuperAdminLocators.protect_alert_message,
                                                            timeout=SuperAdminKeywords.timeout)
        browser.wait_until_page_contains_element(SuperAdminLocators.protect_button,
                                                    timeout=SuperAdminKeywords.timeout)
