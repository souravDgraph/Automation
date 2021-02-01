# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring, unused-argument, too-many-locals, invalid-name
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SlashAPI.components.client.client import Connection
from SlashAPI.components.handlers.utills.utills import Utills
from SlashAPI.components.models.deployment.deployment import DeploymentModels

__all__ = ['Deployments']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Deployments():
    """
    Defines handlers for Deployment related end points

    """

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

        data = Utills.render_data_from_template(DeploymentModels.deployment_attributes,
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '', json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        Deployments.validate_deployment_details(response.json(),
                                                deployment_name,
                                                deployment_zone)
        return response.json()

    @staticmethod
    def delete_deployment(session_alias, url, auth,
                          expected_response=200):

        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.delete_on_session(session_alias,
                                                '',
                                                headers=auth,
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
                          organizationId=None,
                          expected_response=None):
        properties = locals()
        properties_to_delete = ['session_alias', 'url', 'auth', 'expected_response']
        for property_name in properties_to_delete:
            del properties[property_name]
        logger.debug(properties)
        data = Utills.render_data_from_template(DeploymentModels.deployment_attributes,
                                                properties)
        logger.debug(data)

        connection = Connection()
        connection.create_session(session_alias,
                                  url,
                                  auth)
        response = connection.patch_on_session(session_alias,
                                               '',
                                               json=data,
                                               headers=auth,
                                               expected_status=str(expected_response))
        logger.debug(response.json())
        logger.debug(response.text)
        if 'Deployment has been patched.' not in response.text:
            raise Exception("Expected response body not found")
        return response

    @staticmethod
    def backup_ops(session_alias,
                   url,
                   auth,
                   operation,
                   expected_response=None):
        properties = {}
        if operation == "list":
            data = Utills.render_data_from_template(DeploymentModels.list_backup,
                                                    properties)
        elif operation == "create":
            data = Utills.render_data_from_template(DeploymentModels.create_backup,
                                                    properties)
        else:
            raise Exception("Not supported operation")
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        logger.info(response.text)
        if operation == "create" and 'Backup completed.' not in response.text:
            raise Exception("Backup not created")
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
        data = Utills.render_data_from_template(DeploymentModels.freeze_deployment,
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        logger.info(response.text)
        if 'FREEZE OK' not in response.text:
            raise Exception("Deployment not Freezed !")
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
        data = Utills.render_data_from_template(DeploymentModels.deployment_attributes,
                                                properties)
        Utills.compare_dict_based_on_primary_dict_keys(data,
                                                       response_data)

    @staticmethod
    def get_deployments(session_alias,
                        url,
                        auth,
                        expected_response=200):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.get_on_session(session_alias,
                                             '',
                                             headers=auth,
                                             expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def get_deployment_health(session_alias,
                              url,
                              auth):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.get_on_session(session_alias,
                                             '',
                                             headers=auth)
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
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=properties,
                                              headers=auth,
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
        response = connection.get_on_session(session_alias,
                                             '',
                                             headers=auth,
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
        response = connection.delete_on_session(session_alias,
                                                '',
                                                headers=auth,
                                                expected_status=str(expected_response))
        logger.info(response.text)
        if response.text != 'OK':
            raise Exception("Expected response body not found")
