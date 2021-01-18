# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SlashAPI.components.handlers.deployments.deployments import Deployments

__all__ = ['DeploymentKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class DeploymentKeywords():
    """Browser related Keyword Library.

    Main operations:

    - open, close, maximize browser
    """
    @staticmethod
    def create_deployment(session_alias,
                          base_url,
                          auth,
                          deployment_name,
                          deployment_zone,
                          deployment_subdomain=None,
                          organization=None,
                          expected_response=200):
        logger.info("Creating a Deployment of Name : %s" % deployment_name)
        url = base_url + "/deployments/create"
        response = Deployments.create_deployment(session_alias,
                                      url,
                                      auth,
                                      deployment_name,
                                      deployment_zone,
                                      deployment_subdomain,
                                      organization,
                                      expected_response)
        return response

    @staticmethod
    def delete_deployment(session_alias,
                          base_url,
                          auth,
                          deployment_uid,
                          expected_response=200):
        logger.info("Deleting a Deployment of Uid : %s" % deployment_uid)
        url = base_url + "/deployment/" + str(deployment_uid)
        Deployments.delete_deployment(session_alias,
                                      url,
                                      auth,
                                      expected_response)

    @staticmethod
    def get_deployments(session_alias,
                        base_url,
                        auth,
                        expected_response=200):
        logger.info("Get all deployments ")
        url = base_url + "deployments"
        deployments = Deployments.get_deployments(session_alias,
                                      url,
                                      auth,
                                      expected_response)
        return deployments

    @staticmethod
    def get_deployment_health(session_alias,
                        base_url,
                        auth,
                        expected_response=200):
        logger.info("Get health of the deployment ")
        url = base_url + "/health"
        Deployments.get_deployment_health(session_alias,
                                    url,
                                    auth)

    @staticmethod
    def validate_created_deployment( response,
                                     deployment_name,
                                     deployment_zone):
        logger.info("validating deployment")
        Deployments.validate_deployment_details(response, deployment_name, deployment_zone)

    @staticmethod
    def update_deployment(session_alias,
                          base_url,
                          auth,
                          deployment_id,
                          deployment_name=None,
                          deployment_zone=None,
                          deployment_subdomain=None,
                          organization=None,
                          deploymentMode=None,
                          dgraphHA=None,
                          doNotFreeze=None,
                          enterprise=None,
                          isProtected=None,
                          size=None,
                          expected_response=200):
        logger.info("Creating a Deployment of Name : %s" % deployment_id)
        url = base_url + "deployment/" + str(deployment_id)
        response = Deployments.update_deployment(session_alias,
                                                 url,
                                                 auth,
                                                 deployment_name,
                                                 deployment_zone,
                                                 deployment_subdomain,
                                                 organization,
                                                 deploymentMode,
                                                 dgraphHA,
                                                 doNotFreeze,
                                                 enterprise,
                                                 isProtected,
                                                 size,
                                                 expected_response)
        return response

    def get_deployments(session_alias,
                        base_url,
                        auth,
                        expected_response=200):
        logger.info("Get all deployments ")
        url = base_url + "deployments"
        Deployments.get_deployments(session_alias,
                                      url,
                                      auth,
                                      expected_response)

    @staticmethod
    def get_deployment_health(session_alias,
                        base_url,
                        auth,
                        expected_response=200):
        logger.info("Get health of the deployment ")
        url = base_url + "/health"
        Deployments.get_deployment_health(session_alias,
                                    url,
                                    auth)

    @staticmethod
    def backup_ops(session_alias,
                   base_url,
                   auth,
                   operation,
                   expected_response=200):
        logger.info("Backup Operations")
        url = base_url + "/admin/slash"
        response = Deployments.backup_ops(session_alias,
                                          url,
                                          auth,
                                          operation,
                                          expected_response)
        return response


    @staticmethod
    def freeze_ops(session_alias,
                   base_url,
                   auth,
                   deep_freeze='false',
                   backup='true',
                   expected_response=200):
        logger.info("Freeze Operations")
        url = base_url + "/admin/slash"
        response = Deployments.freeze_ops(session_alias,
                                          url,
                                          auth,
                                          deep_freeze,
                                          backup,
                                          expected_response)
        return response

    @staticmethod
    def create_api_key(session_alias,
                   base_url,
                   auth,
                   deployment_id,
                   name,
                   role='admin',
                   expected_response=200):
        logger.info("Create API key for deployment id : %s" % deployment_id)
        url = base_url + "/deployments/" + deployment_id + "/api-keys"
        response = Deployments.create_api_keys(session_alias,
                                          url,
                                          auth,
                                          name,
                                          role,
                                          expected_response)
        return response

    @staticmethod
    def get_api_key(session_alias,
                       base_url,
                       auth,
                       deployment_id,
                       expected_response=200):
        logger.info("Get API key for deployment id : %s " % deployment_id)
        url = base_url + "/deployments/" + deployment_id + "/api-keys"
        response = Deployments.get_api_keys(session_alias,
                                          url,
                                          auth,
                                          expected_response)
        return response

    @staticmethod
    def delete_api_key(session_alias,
                    base_url,
                    auth,
                    deployment_id,
                    api_key_uid,
                    expected_response=200):
        logger.info("Delete  API key of uid %s for deployment id : %s " % (api_key_uid, deployment_id))
        url = base_url + "deployments/" + deployment_id + "/api-keys/" + api_key_uid
        response = Deployments.delete_api_keys(session_alias,
                                            url,
                                            auth,
                                            expected_response)
        return response