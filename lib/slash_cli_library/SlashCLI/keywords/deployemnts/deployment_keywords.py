# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SlashCLI.components.deployments.deployments import Deployments

__all__ = ['DeploymentKeywords']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class DeploymentKeywords:
    """Deployment related Keyword Library.

    Main operations: CRUD

    """

    @staticmethod
    def get_deployments():
        logger.info("Get all deployments ")
        deployments = Deployments.list_deployments(environment="prod")
        return deployments

    @staticmethod
    def create_deployment(environment,
                          deployment_name,
                          region="stgdgraph",
                          subdomain=None,
                          deployment_mode="graphql",
                          expected_return_code=0):
        logger.info("Create new deployment ")
        deployments = Deployments.create_deployment(environment,
                                                    deployment_name,
                                                    region,
                                                    subdomain,
                                                    deployment_mode,
                                                    expected_return_code)
        return deployments

    @staticmethod
    def get_deployment_id_with_endpoint(environment,
                                        endpoint,
                                        expected_return_code=0):
        logger.info("Get deployment id with endpoint %s" % endpoint)
        deployment_id = Deployments.get_deployment_id_with_endpoint(environment,
                                                                    endpoint,
                                                                    expected_return_code)
        return deployment_id

    @staticmethod
    def delete_deployment(environment,
                          deployment_id,
                          skip_confirmation=True,
                          expected_return_code=0):
        logger.info("Deleting deployment with ID  %s" % deployment_id)
        Deployments.delete_deployment(environment,
                                      deployment_id,
                                      skip_confirmation,
                                      expected_return_code)

    @staticmethod
    def get_schema_from_deployment(environment,
                                   deployment_id,
                                   expected_return_code=0):
        logger.info("Get schema of the deployment with ID  %s" % deployment_id)
        Deployments.get_schema_from_deployment(environment,
                                               deployment_id,
                                               expected_return_code)
