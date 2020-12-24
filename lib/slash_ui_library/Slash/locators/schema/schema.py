# !/usr/bin/env python
# coding=utf-8
"""
Author: tkrishnakaushik96@gmail.com
"""


__all__ = ['SettingsLocators']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "tkrishnakaushik96@gmail.com"
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
    security_tab = "xpath = //button[text()='Security']"
    cors_tab = "xpath = //button[text()='CORS']"
    advanced_tab = "xpath = //button[text()='Advanced']"
    backup_tab = "xpath = //button[text()='Backups']"

    backend_mode = "xpath = //h3[normalize-space(text())='Backend Mode']/parent::div"
    select_backend_mode = "xpath = //h3[normalize-space(text())='Backend Mode']//following::div[text()='%s']"
