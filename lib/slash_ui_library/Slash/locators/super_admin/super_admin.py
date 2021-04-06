# !/usr/bin/env python
# coding=utf-8
# pylint: disable=R0903
"""
Author: santhosh@dgraph.io
"""

__all__ = ['SuperAdminLocators']
__author__ = "Santhosh Sekar"
__version__ = "1.0"
__maintainer__ = "Santhosh Sekar"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"


class SuperAdminLocators:
    """
    Base Locators class for super admin page
    """

    list_name = "xpath = //div[text()='%s']"
    search_input_field = "xpath = //input[@placeholder='%s']"
    no_deployment_found = "xpath = //div[text()='No deployments found.']"
    search_btn = "xpath = //button[text()='Search']"
    user_info_label = "xpath = //h3[text()='User Information']"
    deployment_label = "xpath = //h3[text()='backend']/following-sibling::table//div[text()='%s']"
    deployment_link = "xpath = //h3[text()='backend']/following-sibling::table//a[text()='%s']"
    edit_btn = "xpath = //h3[text()='%s']/following-sibling::div//button[text()='Edit']"
    edit_deployment_label = "xpath = //h3[text()=' - Edit Deployment']"
    
    dgraph_lambda_script_label = "xpath = //div[text()='Dgraph Lambda Script']"
    dgraph_lambda_script_tooltip = "xpath = //div[text()='Dgraph Lambda Script']/following-sibling::div//*[local-name()='svg']"
    dgraph_lambda_script_tooltip_message = "xpath = //span[text()='Dgraph Lambda is a serverless platform for running JS on Slash GraphQL (or Dgraph).']"
    dgraph_lambda_script_default_value = "xpath = //div[text()='Dgraph Lambda Script']/following::input[@value='']"
    
    do_not_freeze_label = "xpath = //div[text()='Do Not Freeze']"
    do_not_freeze_tooltip = "xpath = //div[text()='Do Not Freeze']/following-sibling::div//*[local-name()='svg']"
    do_not_freeze_tooltip_message = "xpath = //span[text()='Defaults to False. Set this to True to the prevent the cluster from freezing due to inactivity.']"
    do_not_freeze_value = "xpath = //div[text()='Do Not Freeze']/following::button[1]//div[text()='%s']"
    do_not_freeze_list_value = "xpath = //div[text()='Do Not Freeze']/following::ul[1]//div[text()='%s']"
    
    dgraph_ha_label = "xpath = //div[text()='Dgraph HA']"
    dgraph_ha_tooltip = "xpath = //div[text()='Dgraph HA']/following-sibling::div//*[local-name()='svg']"
    dgraph_ha_tooltip_message = "xpath = //span[text()='Defaults to False. Set this to True for dgraph HA. (Note: You cannot go from HA to non-HA)']"
    dgraph_ha_default_value = "xpath = //div[text()='Dgraph HA']/following::button[1]//div[text()='%s']"
    dgraph_ha_value = "xpath = //div[text()='Dgraph HA']/following::ul[1]//div[text()='%s']"
    
    deployment_mode_label = "xpath = //div[text()='Deployment Mode']"
    deployment_mode_tooltip = "xpath = //div[text()='Deployment Mode']/following-sibling::div//*[local-name()='svg']"
    deployment_mode_tooltip_message = "xpath = //span[text()='Defaults to GraphQL']"
    deployment_mode_graphql_value = "xpath = //div[text()='Deployment Mode']/following::button[1]//div[text()='GraphQL']"
    deployment_mode_value = "xpath = //div[text()='Deployment Mode']/following::ul[1]//div[text()='%s']"
    deployment_mode_link = "xpath = //a[@href='https://dgraph.io/docs/slash-graphql/admin/backend-modes/']"

    deployment_size_label = "xpath = //div[text()='Deployment Size']"
    deployment_size_tooltip = "xpath = //div[text()='Deployment Size']/following-sibling::div//*[local-name()='svg']"
    deployment_size_tooltip_message = "xpath = //span[text()='Defaults to Small']"
    deployment_size_small_value = "xpath = //div[text()='Deployment Size']/following::button[1]//div[text()='Small (1C)']"
    deployment_size_value = "xpath = //div[text()='Deployment Size']/following::ul[1]//div[text()='%s']"
    deployment_size_link = "xpath = //a[@href='https://discuss.dgraph.io/t/slash-deployment-sizing/10635']"

    backup_interval_label = "xpath = //div[text()='Backup Interval']"
    backup_interval_tooltip = "xpath = //div[text()='Backup Interval']/following-sibling::div//*[local-name()='svg']"
    backup_interval_tooltip_message = "xpath = //span[text()='Defaults to 4 hours. Backend data backup frequency']"
    backup_interval_default_value = "xpath = //div[text()='Backup Interval']/following::input[@value='4h']"
    backup_interval_link = "xpath = //a[@href='https://godoc.org/github.com/robfig/cron']"

    backup_bucket_format_label = "xpath = //div[text()='Backup Bucket Format']"
    backup_bucket_format_tooltip = "xpath = //div[text()='Backup Bucket Format']/following-sibling::div//*[local-name()='svg']"
    backup_bucket_format_tooltip_message = 'xpath = //span[contains(text(), "Defaults to '"'%Y-%U'"'. Backup bucket folder name and full backup frequency. Every folder will result in a full backup.")]'
    backup_bucket_format_default_value = "xpath = //div[text()='Backup Bucket Format']/following::input[@value='%Y-%U']"
    backup_bucket_format_link = "xpath = //a[@href='http://www.strfti.me/']"

    jaeger_tracing_label = "xpath = //div[text()='Enable Jaeger Tracing']"
    jaeger_tracing_tooltip = "xpath = //div[text()='Enable Jaeger Tracing']/following-sibling::div//*[local-name()='svg']"
    jaeger_tracing_tooltip_message = "xpath = //span[contains(text(),'Enabled Jaeger Tracing')]"
    jaeger_tracing_default_value = "xpath = //div[text()='Enable Jaeger Tracing']/following::button[1]"
    jaeger_tracing_value = "xpath = //div[text()='Enable Jaeger Tracing']/following::button[1]//div[text()='%s']"
    jaeger_tracing_list_value = "xpath = //div[text()='Enable Jaeger Tracing']/following::ul[1]//div[text()='%s']"

    fields_alert_message = "xpath = //div[text()='%s']/ancestor::div[2]//div[text()='(Altering this field will need cluster restart)']"
    deployment_name_field = "xpath = //h3[text()=' - Edit Deployment']/following::input[@value='%s']"
    enable_acl_default_value = "xpath = //div[text()='Enable ACL']/following::button[1]//div[text()='False']"
    deployment_type_default_value = "xpath = //div[text()='Deployment Type']/following::button[1]//div[text()='Free']"
    protect_button = "xpath = //button[text()='Protect']"
    backup_button = "xpath = //button[text()='Backup']"
    update_button = "xpath = //button[text()='Update']"
    back_button = "xpath = //div[text()='Back']"
    search_deployment_label = "xpath = //h3[text()='Search Deployment']"
    update_alert_message = "xpath = //div[text()='Successfully Updated the backend']"
    protect_alert_message = "xpath = //div[text()='Deployment has been updated']"
    unprotect_button = "xpath = //button[text()='Unprotect']"
    protect_update_alert_message = "xpath = //div[text()='Something went wrong']"