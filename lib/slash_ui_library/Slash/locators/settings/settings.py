# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""


__all__ = ['SettingsLocators']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"

class SettingsLocators:
    """
    Base Locators class for login page
    """

    backend_name = "xpath = //h3[text()='Name']/following-sibling::div/input"

    organization_name = "xpath = //h3[text()='Organization']/following::div"
    organization_select = "xpath = //h3[text()='Organization']/following::button"
    organization = "xpath = //div[text()='%s']/parent::li"

    clone_backend = "xpath = //button[text()='Clone Backend']"
    delete_backend = "xpath = //button[text()='Delete Backend']"
    clone_text = "xpath = //button[text()='Clone Backend']/ancestor::div"
    delete_text = "xpath = //button[text()='Delete Backend']/ancestor::div"
    delete_conformation_input_field = "xpath = //input[@placeholder='Type here (Case sensitive)']"
    destroy_button = "xpath = //button[text()='Destroy']"
    update_button = "xpath = //button[text()='Update']"
    info_tab = "xpath = //button[text()='Info']"
    secutity_tab = "xpath = //button[text()='Info']"
    cors_tab = "xpath = //button[text()='Info']"
    advanced_tab = "xpath = //button[text()='Info']"
    info_tab = "xpath = //button[text()='Info']"
    info_tab = "xpath = //button[text()='Info']"
    info_tab = "xpath = //button[text()='Info']"



