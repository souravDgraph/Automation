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
        logger.info("Creating a Deployment of Name : %s" % deployment_name)
        url = base_url + "graphql"
        response = Deployments.create_deployment(session_alias,
                                                 url,
                                                 auth,
                                                 deployment_name,
                                                 deployment_zone,
                                                 deploymentType,
                                                 dgraphHA,
                                                 size,
                                                 alphaStorage,
                                                 deployment_subdomain,
                                                 organization,
                                                 deploymentMode,
                                                 aclEnabled,
                                                 jaegerEnabled,
                                                 jaegerSize,
                                                 jaegerTrace,
                                                 expected_response)
        return response

    @staticmethod
    def delete_deployment(session_alias,
                          base_url,
                          auth,
                          deployment_uid,
                          expected_response=200):
        logger.info("Deleting a Deployment of Uid : %s" % deployment_uid)
        url = base_url + "graphql"
        Deployments.delete_deployment(session_alias,
                                      url,
                                      auth,
                                      deployment_uid,
                                      expected_response)

    @staticmethod
    def delete_all_deployment(session_alias,
                              base_url,
                              auth,
                              expected_response=200):
        url = base_url + "deployments"
        deployments = Deployments.get_deployments(session_alias,
                                                  url,
                                                  auth,
                                                  expected_response)
        logger.info(type(deployments))

        for deployment in deployments:
            deployment_id = deployment['uid']
            logger.info(deployment_id)
            logger.info("Deleting a Deployment of Uid : %s" % deployment_id)
            url = base_url + "deployment/" + str(deployment_id)
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
    def get_deployment(session_alias, base_url, auth, deployment_id, expected_response_text="OK", expected_response=200):
        logger.info("Get Deployment")
        url = base_url + "graphql"
        deployment = Deployments.get_deployment_with_deployment_id(session_alias, url, auth, deployment_id, expected_response_text, expected_response)

        return deployment

    @staticmethod
    def get_deployment_health(session_alias,
                              base_url,
                              auth,
                              expected_response=200):
        logger.info("Get health of the deployment ")
        url = base_url + "/probe/graphql"
        logger.info(url)
        Deployments.get_deployment_health(session_alias,
                                          url,
                                          auth)

    @staticmethod
    def validate_created_deployment(response,
                                    deployment_name,
                                    deployment_zone,
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
        logger.info("validating deployment")
        Deployments.validate_deployment_details(response,
                                                deployment_name,
                                                deployment_zone,
                                                subdomain,
                                                organization,
                                                deploymentMode,
                                                deploymentType,
                                                size,
                                                alphaStorage,
                                                dgraphHA,
                                                aclEnabled,
                                                jaegerEnabled,
                                                jaegerSize,
                                                jaegerTrace)

    @staticmethod
    def update_deployment(session_alias,
                          base_url,
                          auth,
                          deployment_id,
                          deployment_name=None,
                          deployment_zone=None,
                          deploymentType="free",
                          deployment_subdomain=None,
                          organizationUID=None,
                          deploymentMode=None,
                          dgraphHA=None,
                          doNotFreeze=None,
                          jaegerEnabled=None,
                          size=None,
                          backupInterval=None,
                          backupBucketFormat=None,
                          aclEnabled=None,
                          jaegerSize='0.5',
                          jaegerTrace='0.01',
                          expected_response_text="Successfully Updated the backend",
                          expected_response=200):
        logger.info("Updating a Deployment of Name : %s" % deployment_id)
        url = base_url + "graphql"
        logger.info(url)
        response = Deployments.update_deployment(session_alias,
                                                 url,
                                                 auth,
                                                 deployment_id,
                                                 deployment_name,
                                                 deployment_zone,
                                                 deploymentType,
                                                 deployment_subdomain,
                                                 deploymentMode,
                                                 dgraphHA,
                                                 doNotFreeze,
                                                 jaegerEnabled,
                                                 size,
                                                 organizationUID,
                                                 backupInterval,
                                                 backupBucketFormat,
                                                 aclEnabled,
                                                 jaegerSize,
                                                 jaegerTrace,
                                                 expected_response_text,
                                                 expected_response)
        return response

    @staticmethod
    def get_deployments(session_alias,
                        base_url,
                        auth,
                        expected_response=200):
        logger.info("Get all deployments ")
        url = base_url + "deployments"
        return Deployments.get_deployments(session_alias,
                                      url,
                                      auth,
                                      expected_response)

    @staticmethod
    def update_deployment_protection(session_alias,
                                     base_url,
                                     auth,
                                     backend_uid,
                                     operation,
                                     expected_response=200):
        logger.info("Update Deployment Protection")
        url = base_url + "graphql"
        response = Deployments.update_deployment_protection(session_alias,
                                                            url,
                                                            auth,
                                                            backend_uid,
                                                            operation,
                                                            expected_response)
        return response

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
        url = base_url + "graphql"
        response = Deployments.create_api_keys(session_alias,
                                               url,
                                               auth,
                                               deployment_id,
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
        url = base_url + "graphql"
        response = Deployments.get_api_keys(session_alias,
                                            url,
                                            auth,
                                            deployment_id,
                                            expected_response)
        return response

    @staticmethod
    def delete_api_key(session_alias,
                       base_url,
                       auth,
                       deployment_id,
                       api_key_uid,
                       expected_response_text,
                       expected_response=200):
        logger.info("Delete  API key of uid %s for deployment id : %s " % (api_key_uid, deployment_id))
        url = base_url + "graphql"
        response = Deployments.delete_api_keys(session_alias,
                                               url,
                                               auth,
                                               deployment_id,
                                               api_key_uid,
                                               expected_response_text,
                                               expected_response)
        return response

    @staticmethod
    def update_schema_to_deployment(session_alias,
                                    base_url,
                                    auth,
                                    schema,
                                    expected_response=200):
        logger.info("Updating schema to deployment : %s" % base_url)
        url = base_url + "/admin"
        response = Deployments.update_schema_to_deployment(session_alias,
                                                           url,
                                                           auth,
                                                           schema,
                                                           expected_response)
        return response

    @staticmethod
    def update_rules_to_deployment(session_alias, base_url, auth, deployment_id, rules, expected_response_text="Anon Access updated successfully.", expected_response=200):
        logger.info("Updating rules to deployment id: %s" % deployment_id)
        url = base_url + "graphql"
        response = Deployments.update_rules_to_deployment(session_alias,
                                                            url,
                                                            auth,
                                                            deployment_id,
                                                            rules,
                                                            expected_response_text,
                                                            expected_response)
        return response

    @staticmethod
    def validate_rules_for_deployment(existing_rules, type_name, rule_type="read"):
        logger.info("Validating the existing rules")
        Deployments.validate_rules_for_deployment(existing_rules, type_name, rule_type)

    @staticmethod
    def get_existing_rules(session_alias, base_url, auth, deployment_id, expected_response=200):
        logger.info("Get existing rules for the deployment id: %s" % deployment_id)
        url = base_url + "graphql"
        response = Deployments.get_existing_rules(session_alias,
                                                    url,
                                                    auth,
                                                    deployment_id,
                                                    expected_response)
        return response

    @staticmethod
    def perform_operation_to_database(session_alias,
                                      base_url,
                                      auth,
                                      mutation,
                                      expected_response=200):
        logger.info("perform operation to deployment : %s" % base_url)
        url = base_url + "/graphql"
        response = Deployments.perform_operation_to_database(session_alias,
                                                             url,
                                                             auth,
                                                             mutation,
                                                             expected_response)
        return response

    @staticmethod
    def drop_data_from_database(session_alias,
                                base_url,
                                auth,
                                drop_schema=False,
                                expected_response=200):
        logger.info("Drop all the data from deployment : %s" % base_url)
        url = base_url + "/admin/slash"
        Deployments.drop_data_from_database(session_alias,
                                            url,
                                            auth,
                                            drop_schema,
                                            expected_response)

    @staticmethod
    def get_schema_from_deployment(session_alias,
                                   base_url,
                                   auth,
                                   expected_response=200):
        logger.info("Get schema from deployment : %s" % base_url)
        url = base_url + "/admin"
        response = Deployments.get_schema_from_deployment(session_alias,
                                                          url,
                                                          auth,
                                                          expected_response)
        if response["data"]:
            logger.info(response["data"]["getGQLSchema"]["schema"])
            return response["data"]["getGQLSchema"]["schema"]
        return response