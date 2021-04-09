# !/usr/bin/env python
# coding=utf-8
# pylint: disable=R0903
"""
Author: santhosh@dgraph.io
"""

__all__ = ['SuperAdminLocators']
__author__ = "Santhosh Sekar"
__version__ = "1.0"
__maintainer__ = "Santhosh Sekar"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"


class SuperAdminLocators:
    """
    Base Locators class for super admin page
    """

    list_name = "xpath = //div[text()='%s']"
    search_input_field = "xpath = //input[@placeholder='%s']"
    no_deployment_found = "xpath = //div[text()='%s']"
    error_message = "xpath = //div[text()='There was an error in getting user details']"
    search_btn = "xpath = //button[text()='Search']"
    user_info_label = "xpath = //h3[text()='User Information']"
    deployment_label = "xpath = //h3[text()='backend']/following-sibling::table//div[text()='%s']"
    deployment_link = "xpath = //h3[text()='backend']/following-sibling::table//a[text()='%s']"
    edit_btn = "xpath = //h3[text()='%s']/following-sibling::div//button[text()='Edit']"
    edit_deployment_label = "xpath = //h3[text()=' - Edit Deployment']"
    
    deployment_field_label = "xpath = //div[text()='%s']"
    deployment_field_tooltip = "xpath = //div[text()='%s']/following-sibling::div//*[local-name()='svg']"
    deployment_field_tooltip_message = "xpath = //span[contains(text(),'%s')]"
    deployment_field_value = "xpath = //div[text()='%s']/following::button[1]//div[text()='value']"

    deployment_field_button = "xpath = //div[text()='%s']/following::button[1]"
    deployment_field_list_value = "xpath = //div[text()='%s']/following::ul[1]//div[text()='value']"
    know_more_link = "xpath = //a[@href='%s']"
    deployment_field_input_value = "xpath = //div[text()='%s']/following::input[@value='value']"

    fields_alert_message = "xpath = //div[text()='%s']/ancestor::div[2]//div[text()='(Altering this field will need cluster restart)']"
    deployment_name_field = "xpath = //h3[text()=' - Edit Deployment']/following::input[@value='%s']"
    protect_button = "xpath = //button[text()='Protect']"
    backup_button = "xpath = //button[text()='Backup']"
    update_button = "xpath = //button[text()='Update']"
    back_button = "xpath = //div[text()='Back']"
    search_deployment_label = "xpath = //h3[text()='Search Deployment']"
    unprotect_button = "xpath = //button[text()='Unprotect']"
    alert_message = "xpath = //div[text()='%s']"