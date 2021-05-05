# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""

__all__ = ['LambdaLocators']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"

# pylint: disable=R0903


class LambdaLocators:
    """
    Base Locators class for dashboard page
    """

    # Launch new backend button
    lambda_script = "xpath = //pre[@class=' CodeMirror-line ']//span[@class='cm-comment']"
    logs_tab = "xpath = //button[text()='Logs']"
    script_tab = "xpath = //button[text()='Script']"
    refresh_button = "xpath = //button[text()='Refresh']"
    download_button = "xpath = //button[text()='Download']"
    lambda_info_tab = "xpath = //h3[text()='Learn more']/following-sibling::a"
    save_button = "xpath = //button[text()='Save']"
    delete_button = "xpath = //div[@class='css-1wdzh5i']//button[text()='Delete']"
    popup_delete_button = "xpath = //button[text()='Cancel']//following::button[text()='Delete']"
    filter_button = "xpath = //div[text()='%s']"
    no_lambda_logs_label = "xpath = //div[text()='No logs for this backend to show']"

    # Javascript
    get_lambdas = "return document.getElementsByClassName('CodeMirror-lines').valueOf()[0].innerText"
    get_lambdas_logs = "return document.getElementsByClassName('css-i3xp0b').valueOf()[0].textContent"
