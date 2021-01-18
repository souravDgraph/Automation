# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments
"""
Author: vivetha@dgraph.io
"""
import os

from robot.api import logger
from SlashAPI.components.client.client import Connection
from SlashAPI.components.handlers.utills.utills import Utills


__all__ = ['Deployments']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Deployments():

    deployment_details_template_file = "deployment_attributes.txt"
    create_deployment_template_file = "create_deployment.txt"
    list_backups_template_file = "list_backups.txt"
    create_backup_template_file = "create_backup.txt"
    freeze_template_file = "freeze_deployment.txt"

    @staticmethod
    def create_deployment(session_alias,
                          url,
                          auth,
                          deployment_name,
                          deployment_zone,
                          deployment_subdomain=None,
                          organization=None,
                          expected_response=200):
        properties = {"name": deployment_name, "zone": deployment_zone}
        if deployment_subdomain:
            properties["subdomain"] = deployment_subdomain
        if organization:
            properties["organization"] = organization

        data = Utills.render_data_from_template(Utills.render_template_path(Deployments.create_deployment_template_file),
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias, '', json=data, headers=auth,
                                                  expected_status=str(expected_response))
        Deployments.validate_deployment_details(response.json(), deployment_name, deployment_zone)
        return response.json()

    @staticmethod
    def delete_deployment(session_alias, url, auth,
                          expected_response=200):

        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.delete_on_session(session_alias, '', headers=auth,
                                                expected_status=str(expected_response))
        logger.info(response.json)

    @staticmethod
    def update_deployment(session_alias,
                          url,
                          auth,
                          name=None,
                          zone=None,
                          subdomain=None,
                          organization=None,
                          deploymentMode=None,
                          dgraphHA=None,
                          doNotFreeze=None,
                          enterprise=None,
                          isProtected=None,
                          size=None,
                          expected_response=None):
        properties = locals()
        properties_to_delete = ['session_alias', 'url', 'auth', 'expected_response']
        for property in properties_to_delete:
            del properties[property]
        data = Utills.render_data_from_template(
            Utills.render_template_path(Deployments.create_deployment_template_file),
            properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.patch_on_session(session_alias, '', json=data, headers=auth,
                                                expected_status=str(expected_response))
        logger.info(response.json())

    @staticmethod
    def backup_ops(session_alias,
                   url,
                   auth,
                   operation,
                   expected_response=None):
        properties = {}
        if operation == "list":
            data = Utills.render_data_from_template(Utills.render_template_path(Deployments.list_backups_template_file),
                                                    properties)
        elif operation == "create":
            data = Utills.render_data_from_template(Utills.render_template_path(Deployments.create_backup_template_file),
                                                    properties)
        else:
            raise Exception("Not supported operation")
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias, '', json=data, headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def freeze_ops(session_alias,
                   url,
                   auth,
                   deep_freeze,
                   backup,
                   expected_response=None):
        properties = {
            "deep_freeze": deep_freeze,
            "backup": backup
        }
        data = Utills.render_data_from_template(Utills.render_template_path(Deployments.freeze_template_file),
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias, '', json=data, headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def validate_deployment_details(response_data,
                                    name,
                                    zone,
                                    subdomain=None,
                                    organization=None,
                                    deploymentMode='graphql',
                                    dgraphHA='false',
                                    doNotFreeze='false',
                                    enterprise='false',
                                    isProtected='false',
                                    size='small'):
        properties = locals()
        del properties["response_data"]
        data = Utills.render_data_from_template(Utills.render_template_path(Deployments.deployment_details_template_file),
                                                properties)
        Utills.compare_dict_based_on_primary_dict_keys(data, response_data)
        
    @staticmethod
    def get_deployments(session_alias,
                        url,
                        auth,
                        expected_response=200):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.get_on_session(session_alias, '', headers=auth,
                                            expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def get_deployment_health(session_alias,
                        url,
                        auth):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.get_on_session(session_alias, '', headers=auth)
        logger.info(response.json())

    @staticmethod
    def create_api_keys(session_alias,
                   url,
                   auth,
                   name,
                   role,
                   expected_response=None):
        properties = {
            "name": name,
            "role": role
        }

        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias, '', json=properties, headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def get_api_keys(session_alias,
                        url,
                        auth,
                        expected_response=None):

        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.get_on_session(session_alias, '',headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def delete_api_keys(session_alias,
                     url,
                     auth,
                     expected_response=None):

        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.delete_on_session(session_alias, '', headers=auth,
                                             expected_status=str(expected_response))
        logger.info(response.text)
        if response.text != 'OK':
            raise Exception("Expected response body not found")
        logger.info(response.json)




