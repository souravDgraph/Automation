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
    starter_product_disabled = "xpath = //div[text()='Select a product type']/following::button[@disabled]"
    organization_name = "xpath = //div[text()='%s']/parent::li"
    provider = "xpath = //img[@alt='AWS']/parent::div"
    zone = "xpath = //div[text()='%s']"
    launch_button = "xpath = //button[text()='Launch']"
    backend_live = "xpath = //h3[text()='Your Backend is live!']"
    spinning_backend = "xpath = //h3[text()='Creating your backend']"
    create_schema_button = "xpath = //button[text()='Create your Schema']"
    backend_endpoint = "xpath =//div[@title='Creating Backend']//input"
    backend_listbox = "xpath =//button[@aria-haspopup='listbox']"
    graphql_schema_button = "xpath = //button[text()='GraphQL Schema']"
    graphql_endpoint = "xpath = //*[contains(@value,'%s')]"
    avatar_button = "xpath =//button//img[@alt='avatar']"
    cluster_usage = "xpath =//div[text()='Cluster Usage']"
    logout = "xpath = //button[text()='Log out']"
    schema_label = "xpath = //h3[text()='Schema']"
    lambdas_label = "xpath = //h3[text()='Lambdas']"
    settings_label = "xpath = //h3[text()='Settings']"
    api_explorer_label = "xpath = //div[text()='Explorer']"
    launch_new_backend_label = "xpath = //h3[text()='Launch a New Backend']"
    deployment_location = "xpath = //div[text()='%s']"
    add_card_number = "xpath = //input[@name='cardnumber']"
    iframe_element = "xpath = //div//iframe[contains(@name,'__privateStripeFrame')]"
    expiry_date = "xpath = //input[@name='exp-date']"
    cvc = "xpath = //input[@name='cvc']"
    postal = "xpath = //input[@name='postal']"
    add_button = "xpath = //h3[text()='Add Credit Card']//following::button[text()='Add']"
    cancel_subscription_button = "xpath = //button[text()='Cancel Subscription']"
    cancel_subscription_confirm_button = "xpath = //button[text()='Confirm']"
    card_added_alert_message = "xpath = //div[text()='Added payment details successfully']"
    card_cancelled_alert_message = "xpath = //div[text()='Cancelling subscription...']"
    no_active_subscription_label = "xpath = //h3[text()='No active subscriptions']"
    billing_button = "xpath = //button[text()='Billing']"
    billing_label = "xpath = //h3[text()='Billing']"

    # Menu items
    schema = "xpath = //a[@href='/_/schema']"
    settings = "xpath = //a[@href='/_/settings']"
    lambdas = "xpath = //a[@href='/_/lambdas']"
    api_explorer = "xpath = //a[@href='/_/explorer']"
    overview = "xpath = //a[@href='/_/dashboard']"
    documentation = "xpath = //a[@href='https://dgraph.io/docs/slash-graphql/slash-quick-start/']"

    backends_list = "xpath = //button[@aria-haspopup='listbox']"
    backend_selection = "xpath = //li/div[text()='RC3']"
