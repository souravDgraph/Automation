# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring, redefined-builtin
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SlashCLI.components.utils.utils import Utils
from SlashCLI.components.deployments.constants import DeploymentConstants

__all__ = ['Deployments']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Deployments:

    """
    Defines handlers for Deployment related end points

    """
    @staticmethod
    def list_deployments(environment,
                         quiet=None,
                         extended=None,
                         filter=None,
                         sort=None,
                         csv=None,
                         columns=None,
                         no_header=None,
                         no_truncate=None,
                         output=None,
                         expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["expected_return_code"]
        base_command = "list-backends"
        options = ""
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
                options += " --" + key + "=" + properties[key]

        logger.info(base_command)
        logger.info(options)
        output, _ = Utils.execute_slash_graphql_command(base_command, options)
        return output

    @staticmethod
    def create_deployment(environment,
                          deployment_name,
                          type="slash-graphql",
                          region="stgdgraph",
                          organizationId=None,
                          subdomain=None,
                          mode="graphql",
                          acl=None,
                          organizationId=None,
                          dgraphHA=None,
                          size=None,
                          jaeger=None,
                          storage=None,
                          dataFile=None,
                          gqlSchemaFile=None,
                          schemaFile=None,
                          expected_output_text=None,
                          expected_return_code=0):
        properties = locals()
        properties_to_exclude = ['deployment_name', "expected_return_code", "expected_output_text"]
        base_command = "deploy-backend "
        options = deployment_name
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
                options += " --" + key + "=" + properties[key]

        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
        if expected_output_text not in str(output) and expected_return_code == 0:
            raise Exception("Deployment not create as expected" and not error)
        elif expected_output_text not in str(error) and expected_return_code != 0:
            raise Exception("Expected error message not found")

        if expected_return_code == 0:
            details = output.split("Launched at: ")
            return details[1].replace("\\n'", "")

    @staticmethod
    def update_deployment(environment,
                          endpoint,
                          deployment_name=None,
                          mode="graphql",
                          acl=None,
                          organizationId=None,
                          token=None,
                          skip_confirmation=True,
                          expected_return_code=0):
        properties = locals()
        properties_to_exclude = ['deployment_name', "expected_return_code"]
        base_command = "deploy-backend "
        options = deployment_name
        if skip_confirmation:
            options += " --confirm"
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
                options += " --" + key + "=" + properties[key]

        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)

    @staticmethod
    def get_deployment_id_with_endpoint(environment,
                                        endpoint,
                                        expected_return_code=0):
        deployment_details = Deployments.list_deployments(environment,
                                                          expected_return_code)
        deployments = deployment_details.split("\\n")
        for deployment in deployments:
            if endpoint in deployment:
                logger.info(deployment)
                deployment_details = deployment.split(" ")
                deployment_id = deployment_details[0]
                logger.info(deployment_id)
        return deployment_id

    @staticmethod
    def delete_deployment(environment,
                          deployment_id,
                          skip_confirmation=True,
                          expected_output_text=None,
                          expected_return_code=0):
        base_command = "destroy-backend " + deployment_id
        options = " --environment=" + environment
        if skip_confirmation:
            options += " --confirm"
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
        if expected_output_text not in str(output) and not error:
            raise Exception("Deployment was not deleted as expected")

    @staticmethod
    def get_schema_from_deployment(environment,
                                   endpoint,
                                   expected_output_text,
                                   expected_return_code=0):
        properties = locals()
        properties_to_exclude = [ "expected_output_text", "expected_return_code" ]
        base_command = "get-schema"
        options = ""
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
                options += " --" + key + "=" + str(properties[key])
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
        if expected_output_text not in str(output) and expected_return_code == 0:
            raise Exception("Unable to Fetch Schema" and not error)
        elif expected_output_text not in str(error) and expected_return_code != 0:
            raise Exception("Expected error message not found")
        return output

    @staticmethod
    def list_backups(environment,
                     endpoint,
                     expected_output_text,
                     expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["expected_return_code", "expected_output_text"]
        base_command = "list-backups"
        options = ""
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
                options += " --" + key + "=" + str(properties[key])
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
        if expected_output_text not in str(output) and expected_return_code == 0:
            raise Exception("Unable to Fetch Backups" and not error)
        elif expected_output_text not in str(error) and expected_return_code != 0:
            raise Exception("Expected error message not found")
        return output

    @staticmethod
<<<<<<< HEAD
    def get_lambda(environment,
                   endpoint,
                   expected_return_code=0):
        properties = locals()
        base_command = "get-lambda"
        options = ""
        for key in properties.keys():
            if properties[key]:
                options += " --" + key + "=" + str(properties[key])
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
=======
    def update_deployment(environment, endpoint,
                                        mode,
                                        name,
                                        organizationId,
                                        token,
                                        skip_confirmation,
                                        expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["skip_confirmation", "expected_return_code"]
        base_command = "update-backend"
        options = ""
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
                logger.info(type(key))
                logger.info(properties[key])
                logger.info(type(options))
                options += " --" + key + "=" + properties[key]
        if skip_confirmation:
            options += " --confirm"
        logger.info(base_command)
        logger.info(options)
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
        logger.info(error)
>>>>>>> Added Test Cases For Slash CLI
        return output