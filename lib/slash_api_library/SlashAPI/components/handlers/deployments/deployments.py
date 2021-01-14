# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments
"""
Author: vivetha@dgraph.io
"""

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

    @staticmethod
    def create_deployment(session_alias, url, auth,
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





