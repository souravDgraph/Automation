"""
Author: vivetha@dgraph.io
"""
# pylint: disable=C0301, R0903, line-too-long

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
    create_api_key_button = "xpath = //button[text()='Create New']"
    enter_api_name_textbox = "xpath = //input[@placeholder='Name']"
    create_api_button = "xpath = //button[text()='Create']"
    api = "xpath = //div[text()='%s']"
    okay_button = "xpath = //div//button[text()='Okay']"
    delete_button = "xpath = //div[text()='%s']/following::button[text()='Delete']"
    delete_api_key_confirm = "xpath = //h3[text()='Delete API Key']/following::button[text()='Continue']"
    update_button = "xpath = //button[text()='Update']"
    info_tab = "xpath = //button[text()='Info']"
    security_tab = "xpath = //button[text()='Security']"
    cors_tab = "xpath = //button[text()='CORS']"
    advanced_tab = "xpath = //button[text()='Advanced']"
    backup_tab = "xpath = //button[text()='Backups']"
    api_keys_tab = "xpath = //button[text()='API Keys']"

    backend_mode = "xpath = //h3[normalize-space(text())='Backend Mode']/parent::div"
    select_backend_mode = "xpath = //h3[normalize-space(text())='Backend Mode']//following::div[text()='%s']"
