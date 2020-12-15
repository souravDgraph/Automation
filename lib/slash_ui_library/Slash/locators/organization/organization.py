# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""


__all__ = ['OrganizationLocators']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"

class OrganizationLocators:
    """
    Base Locators class for dashboard page
    """

    # Launch new backend button

    add_button = "xpath = //button[text()='Add']"
    org_list = "xpath = //tbody"
    org_list_headers = "xpath = //thead"
    org = "xpath = //a[text()='%s']"
    leave_org = "xpath = //div[text()='%s']/following::button[text()='Leave']"
    add_member = "xpath = //button[text()='Add Member']"
    remove_org = "xpath = //div[text()='%s']/following::button[text()='Remove']"
    org_email = "xpath = //input[@placeholder='Email ID used for slash account']"
    add_member_alert = "xpath = //h3[text()='Unable to add member']/following-sibling::div"



















