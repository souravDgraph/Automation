"""
Author: santhosh@dgraph.com
"""

__all__ = ['SchemaLocators']
__author__ = "Santhosh S"
__version__ = "1.0"
__maintainer__ = "Santhosh S"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"


class ApiExplorerLocators:
    """
    Base Locators class
    """

    dropdown_list = "xpath = //form//select"
    add_button = "xpath = //button[@type='submit']//span"
    execute_query_button = "xpath = //button[@title='Execute Query (Ctrl-Enter)']"
    add_mutation_span = "xpath = //span[text()='%s']"
    field_checkbox = "xpath = //span[text()='%s']"
    field_input_textbox = "xpath = //div[@data-arg-name='%s']//following-sibling::input"
    query_label = "xpath = //div[text()='%s']"
    remove_query_button = "xpath = //div[text()='%s']//descendant::button[1]"

    #javascript
    get_scroll_height = "return document.getElementsByClassName('CodeMirror-scroll')[2].scrollHeight"
    set_scroll_top = 'document.getElementsByClassName("CodeMirror-scroll")[2].scrollTop=%s'
    get_query_data = "return document.getElementsByClassName('CodeMirror-lines').valueOf()[2].innerText.toString()"