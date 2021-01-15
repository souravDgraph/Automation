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
    def validate_created_deployment( response,
                                     deployment_name,
                                     deployment_zone):
        logger.info("validating deployment")
        Deployments.validate_deployment_details(response, deployment_name, deployment_zone)

    @staticmethod
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

