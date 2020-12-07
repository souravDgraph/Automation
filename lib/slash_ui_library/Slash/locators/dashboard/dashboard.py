# !/usr/bin/env python
# coding=utf-8
"""
Author: vivetha@dgraph.io
"""


__all__ = ['DashboardLocators']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"



class DashboardLocators:
    """
    Base Locators class for dashboard page
    """

    # Launch new backend button
    create_backend = "xpath = //button[text()='Launch new backend']"
    backend_name = "xpath = //h3[text()='Name']/following-sibling::input"
    subdomain = "xpath = //h3[text()='Subdomain']/following-sibling::input"
    organization_select = "xpath = //div[text()='Select organization']/ancestor::button"
    organization_name = "xpath = //div[text()='%s']/parent::li"
    provider = "xpath = //img[@alt='AWS']/parent::div"
    zone = "xpath = //div[text()='%s']/parent::div"
    launch_button = "xpath = //button[text()='Launch']"
    backend_live = "xpath =//h3[text()='Your Backend is live!']"
    spinning_backend = "xpath = //h3[text()='Your Backend is spinning up...']/parent::div"
    create_schema_button = "xpath = //button[text()='Create your Schema']"
    backend_endpoint = "xpath =//div[@title='Creating Backend']//input"

    # Menu items
    schema = "xpath = //a[@href='/_/schema']"
    settings = "xpath = //a[@href='/_/settings']"




