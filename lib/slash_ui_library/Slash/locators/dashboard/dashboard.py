# !/usr/bin/env python
# coding=utf-8
# pylint: disable=R0903
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
    backend_name = "xpath = //input[@placeholder='Name']"
    subdomain = "xpath = //h3[text()='Subdomain']/following-sibling::input"
    organization_select = "xpath = //div[text()='Select organization']/ancestor::button"
    select_product = "xpath = //h3[text()='%s']"
    organization_name = "xpath = //div[text()='%s']/parent::li"
    provider = "xpath = //img[@alt='AWS']/parent::div"
    zone = "xpath = //div[text()='%s']"
    launch_button = "xpath = //button[text()='Launch']"
    backend_live = "xpath = //h3[text()='Your Backend is live!']"
    spinning_backend = "xpath = //div[text()='Your Backend is spinning up...']"
    create_schema_button = "xpath = //button[text()='Create your Schema']"
    backend_endpoint = "xpath =//div[@title='Creating Backend']//input"
    backend_listbox = "xpath =//button[@aria-haspopup='listbox']"
    graphql_schema_button = "xpath = //button[text()='GraphQL Schema']"
    graphql_endpoint = "xpath = //input[@value='%s']"
    deployment_location = "xpath = //h3[text()=' Deployment Info']/following::div[text()='Location : %s']"
    graphql_guide = "xpath = //a[@href='%s']"
    quick_start_video = "xpath = //button//h3[text()='Quick Start Video']"

    # Menu items
    schema = "xpath = //a[@href='/_/schema']"
    settings = "xpath = //a[@href='/_/settings']"
    lambdas = "xpath = //a[@href='/_/lambdas']"
    api_explorer = "xpath = //a[@href='/_/explorer']"
    overview = "xpath = //a[@href='/_/dashboard']"
    usage_metrics = "xpath = //a[@href='/_/usage']"
    documentation = "xpath = //a[@href='https://dgraph.io/docs/slash-graphql/slash-quick-start/']"

    backends_list = "xpath = //button[@aria-haspopup='listbox']"
    backend_selection = "xpath = //li/div[text()='RC3']"
