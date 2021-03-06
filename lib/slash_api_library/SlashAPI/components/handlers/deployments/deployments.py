# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring, unused-argument, too-many-locals, invalid-name
"""
Author: vivetha@dgraph.io
"""

from robot.api import logger
from SlashAPI.components.client.client import Connection
from SlashAPI.components.handlers.utils.utils import Utils
from SlashAPI.components.models.deployment.deployment import DeploymentModels
import requests, time, json

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
                          deploymentType="free",
                          dgraphHA='false',
                          size="medium",
                          alphaStorage='40',
                          deployment_subdomain=None,
                          organization=None,
                          deploymentMode="graphql",
                          aclEnabled='false',
                          jaegerEnabled='false',
                          jaegerSize='0.5',
                          jaegerTrace='0.01',
                          expected_response=200):
        properties = {"name": deployment_name, "zone": deployment_zone, "deploymentType" : deploymentType}
        if deploymentType == "dedicated":
            ha_properties = {"size" : size,
                             "alphaStorage" : alphaStorage,
                             "dgraphHA" : dgraphHA,
                             "aclEnabled": aclEnabled,
                             "jaegerEnabled": jaegerEnabled,
                             "jaegerSize": jaegerSize,
                             "jaegerTrace": jaegerTrace}
            properties.update(ha_properties)
        else:
            size = "small"
            alphaStorage = "10Gi"
        if deployment_subdomain:
            properties["subdomain"] = deployment_subdomain
        if organization:
            properties["organization"] = organization

        data = Utils.render_data_from_template(DeploymentModels.create_deployment,
                                                properties)
        logger.info("-*-*-*"*40)
        logger.info(data)
        logger.info("-*-*-*" * 40)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        deployment_details = response.json()['data']['createDeployment']
        Deployments.validate_deployment_details(deployment_details,
                                                deployment_name,
                                                deployment_zone,
                                                deployment_subdomain,
                                                organization,
                                                deploymentMode,
                                                deploymentType,
                                                size,
                                                alphaStorage,
                                                dgraphHA,
                                                aclEnabled,
                                                jaegerEnabled,
                                                jaegerSize,
                                                jaegerTrace
                                                )
        logger.info(deployment_details)
        return deployment_details

    @staticmethod
    def delete_deployment(session_alias,
                          url,
                          auth,
                          backend_uid,
                          expected_response=200):
        properties = {"deploymentID": backend_uid}
        data = Utils.render_data_from_template(DeploymentModels.delete_deployment,
                                               properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                                '',
                                                json=data,
                                                headers=auth,
                                                expected_status=str(expected_response))
        logger.info(response.json)

    @staticmethod
    def update_deployment(session_alias,
                          url,
                          auth,
                          uid,
                          name=None,
                          zone=None,
                          subdomain=None,
                          deploymentMode=None,
                          deploymentType="free",
                          dgraphHA=None,
                          doNotFreeze=None,
                          jaegerEnabled=None,
                          size=None,
                          organizationUID=None,
                          backupInterval=None,
                          backupBucketFormat=None,
                          aclEnabled=None,
                          jaegerSize='0.5',
                          jaegerTrace='0.01',
                          expected_response_text="Successfully Updated the backend",
                          expected_response=None):
        properties = locals()
        logger.info(properties)
        properties_to_delete = ['session_alias', 'url', 'auth', 'expected_response', 'expected_response_text']
        for property_name in properties_to_delete:
            del properties[property_name]
        logger.debug(properties)
        data = Utils.render_data_from_template(DeploymentModels.update_deployment,
                                               properties)
        connection = Connection()
        connection.create_session(session_alias,
                                  url,
                                  auth)
        response = connection.post_on_session(session_alias,
                                               '',
                                               json=data,
                                               headers=auth,
                                               expected_status=str(expected_response))
        logger.debug(response.json())
        logger.debug(response.text)
        if "errors" in response.json() and response.json()["errors"][0]["message"] != expected_response_text:
            raise Exception("Expected error not found")
        elif response.json()["data"] and expected_response_text not in str(response.text):
            raise Exception("Expected response body is not found")
        return response

    @staticmethod
    def update_deployment_protection(session_alias,
                                     url,
                                     auth,
                                     backend_uid,
                                     operation,
                                     expected_response=None):
        properties = {"uid": backend_uid}
        data = Utils.render_data_from_template(DeploymentModels.protect_deployment,
                                               properties)
        if operation.lower() == "protect":
            data["variables"]["input"]["protect"] = True
        elif operation.lower() == "unprotect":
            data["variables"]["input"]["protect"] = False
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
        return response.json()

    @staticmethod
    def backup_ops(session_alias,
                   url,
                   auth,
                   operation,
                   expected_response=None):
        properties = {}
        if operation == "list":
            data = Utils.render_data_from_template(DeploymentModels.list_backup,
                                                    properties)
        elif operation == "create":
            data = Utils.render_data_from_template(DeploymentModels.create_backup,
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
        if operation == "create" and 'Backup completed.' not in response.text :
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
        data = Utils.render_data_from_template(DeploymentModels.freeze_deployment,
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
        if 'FREEZE OK' not in response.text :
            raise Exception("Deployment not Freezed !")
        return response.json()

    @staticmethod
    def validate_deployment_details(response_data,
                                    name,
                                    zone,
                                    subdomain=None,
                                    organization=None,
                                    deploymentMode='graphql',
                                    deploymentType="free",
                                    size="small",
                                    alphaStorage="10",
                                    dgraphHA="false",
                                    aclEnabled='false',
                                    jaegerEnabled='false',
                                    jaegerSize='0.5',
                                    jaegerTrace='0.01'
                                    ):
        properties = locals()
        logger.info(properties)
        del properties["response_data"]
        data = Utils.render_data_from_template(DeploymentModels.deployment_attributes, properties)
        Utils.compare_dict_based_on_primary_dict_keys(data, response_data)

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
    def get_deployment_with_deployment_id(session_alias, url, auth, deployment_id, expected_response_text="OK", expected_response=200):
        properties = {
            "deployment_id": deployment_id
        }
        data = Utils.render_data_from_template(DeploymentModels.get_deployment,
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias, '',
                                                json=data,
                                                headers=auth,
                                                expected_status=str(expected_response))

        logger.info(response.text)
        if "errors" in response.json() and response.json()["errors"][0]["message"] != expected_response_text:
            raise Exception("Expected error not found")
        elif "errors" not in response.json() and expected_response_text not in response.reason:
            raise Exception("Expected Body Response is not Found")
        logger.info(response.json())
        return response.json()

    @staticmethod
    def get_deployment_health(session_alias,
                              url,
                              auth,
                              expected_response=200):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        for cycle in range(1, 20):
            response_code = requests.get(url, headers=auth)
            logger.info(response_code)
            logger.info(type(response_code.status_code))
            if int(response_code.status_code) == expected_response:
                break
            time.sleep(10)

    @staticmethod
    def create_api_keys(session_alias,
                        url,
                        auth,
                        deployment_id,
                        name,
                        role,
                        expected_response=None):
        properties = {
            "deploymentID": deployment_id,
            "name": name,
            "role": role
        }
        data = Utils.render_data_from_template(DeploymentModels.create_api_key,
                                               properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def get_api_keys(session_alias,
                     url,
                     auth,
                     deployment_id,
                     expected_response=None):
        properties = {
            "deploymentID": deployment_id
        }
        data = Utils.render_data_from_template(DeploymentModels.get_api_key,
                                               properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def delete_api_keys(session_alias,
                        url,
                        auth,
                        deployment_id,
                        api_key_id,
                        expected_response_text,
                        expected_response=None):
        properties = {
            "deploymentID" : deployment_id,
            "apiKeyID" : api_key_id
        }
        data = Utils.render_data_from_template(DeploymentModels.delete_api_key,
                                               properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.text)
        if expected_response_text not in response.text :
            raise Exception("Expected response body not found")

    @staticmethod
    def update_schema_to_deployment(session_alias,
                                    url,
                                    auth,
                                    schema,
                                    expected_response=None):
        properties = {
            "schema": schema
        }
        data = Utils.render_data_from_template(DeploymentModels.update_schema,
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def update_rules_to_deployment(session_alias, url, auth, deployment_id, rules, expected_response_text, expected_response=None):
        properties = {
            "anonAccess" : rules,
            "deploymentID" : deployment_id
        }
        data = Utils.render_data_from_template(DeploymentModels.update_rules, properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                                '',
                                                json=data,
                                                headers=auth,
                                                expected_status=str(expected_response))

        logger.info(response.json())
        if expected_response_text != response.json()["data"]["updateDeploymentAnonAccess"]:
            raise Exception("Expected response body not found")
        return response.json()

    @staticmethod
    def validate_rules_for_deployment(existing_rules, type_name, rule_type):
        properties = {
            "type" : type_name
        }
        if(rule_type=="read"):
            data = Utils.render_data_from_template(DeploymentModels.read_rules_attributes, properties)
        elif(rule_type=="write"):
            data = Utils.render_data_from_template(DeploymentModels.write_rules_attributes, properties)
        logger.info(data)
        if data != json.loads(existing_rules["data"]["getDeploymentByID"]["anonAccess"]):
            raise Exception("Expected data not found")

    @staticmethod
    def get_existing_rules(session_alias, url, auth, deployment_id, expected_response=None):
        properties = {
            "deploymentID" : deployment_id
        }
        data = Utils.render_data_from_template(DeploymentModels.get_rules, properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                                '',
                                                json=data,
                                                headers=auth,
                                                expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def perform_operation_to_database(session_alias,
                                      url,
                                      auth,
                                      mutation,
                                      expected_response=None):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              data=mutation,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()

    @staticmethod
    def drop_data_from_database(session_alias,
                                url,
                                auth,
                                drop_schema=False,
                                expected_response=None):
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        if drop_schema:
            payload = DeploymentModels.drop_schema_and_data
        else:
            payload = DeploymentModels.drop_data
        response = connection.post_on_session(session_alias,
                                              '',
                                              data=payload,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        if 'Done' not in response.text or 'Success' not in response.text:
            raise Exception("Expected response body not found")


    @staticmethod
    def get_schema_from_deployment(session_alias,
                                   url,
                                   auth,
                                   expected_response=None):
        properties = {}
        data = Utils.render_data_from_template(DeploymentModels.get_schema,
                                                properties)
        connection = Connection()
        connection.create_session(session_alias, url, auth)
        response = connection.post_on_session(session_alias,
                                              '',
                                              json=data,
                                              headers=auth,
                                              expected_status=str(expected_response))
        logger.info(response.json())
        return response.json()