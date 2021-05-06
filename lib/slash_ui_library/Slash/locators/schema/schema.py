"""
Author: tkrishnakaushik96@gmail.com
"""

__all__ = ['SchemaLocators']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Production"


class SchemaLocators:
    """
    Base Locators class for login page
    """

    schema_editor_button = "xpath = //button[text()='Schema Editor']"
    builder_mode_button = "xpath = //button[text()='Builder Mode']"

    add_type_button = "xpath = //button/following::div[text()='Add Type']"
    # Add Type elements
    name_text_box = "css = [placeholder='Name']"

    add_user_button = "xpath = //*[text()='Add Enum']"

    graphql_schema_button = "xpath = //button[text()='GraphQL Schema']"
    ui_mode_button = "xpath = //button[text()='Switch to UI Mode']"
    text_mode_button = "xpath = //button[text()='Switch to Text Mode']"
    inspect_panel_label = "xpath = //h3[text()='Inspect Panel']"
    deploy_button = "xpath = //button[text()='Deploy']"
    okay_button = "xpath = //h3[text()='Success']/ancestor::div//button[text()='Okay']"
    add_button = "xpath = //button/following::div[text()='Add']"
    default_type_name = "xpath = //div/ancestor::div//h3[text()='%s']"
    editable_type_name = "xpath = //div//following::input[@value='%s']"
    save_button = "xpath = //input//following::button[text()='Save']"
    add_field_button = "xpath = //h3[text()='%s']//following::button[@class='css-zt53j8']"
    editable_field_name = "xpath = //h3[text()='%s']//following::input[@value='old_field_name']"
    field_type_button = "xpath = //h3[text()='%s']//following::div//input[@value='untitledfield']//following-sibling::div//button//div[text()='old_data_type']"
    select_field_type = "xpath = //h3[text()='%s']//following::div//input[@value='field_name']//following-sibling::div//button//following::li//div[text()='new_data_type']"
    edit_button = "xpath = //*[local-name()='svg' and @viewBox='0 0 16 13']//parent::button"
    delete_type_button = "xpath = //*[local-name()='svg' and @viewBox='0 0 11 14']//parent::button"
    drop_data_button = "xpath = //button[text()='Drop Data']"
    drop_all_data_button = "xpath = //button[text()='Drop All Data']"
    success_okay_button = "xpath = //div[text()='Successfully dropped backend data.']//following-sibling::div//button[text()='Okay']"
    success_drop_field_okay_button = "xpath = //div[text()='Successfully dropped selected types/fields']//following-sibling::div//button[text()='Okay']"
    remove_type_confirm_button = "xpath = //button[text()='Remove']"
    unused_fields = "xpath = //div[text()='%s']"
    drop_data_cancel_button = "xpath = //h3[text()='Drop Data']//following::div//button[text()='Cancel']"
    drop_button = "xpath = //button[text()='Drop']"
    drop_data_label = "xpath = //h3[text()='Drop Data']"
    remove_field_button = "xpath = //button[text()='Remove Field']"

    # Javascript
    get_schema = "return document.getElementsByClassName('CodeMirror-code').valueOf()[0].textContent"
    