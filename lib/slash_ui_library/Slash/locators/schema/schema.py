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

    add_type_button = "xpath = //*[text()='Add Type']"
    # Add Type elements
    name_text_box = "css = [placeholder='Name']"

    add_user_button = "xpath = //*[text()='Add Enum']"
