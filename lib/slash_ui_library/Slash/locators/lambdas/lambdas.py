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

class LambdaLocators:
    """
    Base Locators class for dashboard page
    """

    # Launch new backend button
    lambda_script = "cm-comment"
    logs_tab = "xpath = //button[text()='Logs']"
    script_tab = "xpath = //button[text()='Script']"
    refresh_tab = "xpath = //button[text()='Refresh']"
    download_tab = "xpath = //button[text()='Download']"
    lambda_info_tab = "xpath = //h3[text()='Learn more']/following-sibling::a"











