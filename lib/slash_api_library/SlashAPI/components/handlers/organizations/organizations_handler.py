# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, W0201, C0301
"""
Author: krishna@dgraph.io
"""
from robot.api import logger
from robot.utils.asserts import assert_equal
from SlashAPI.components.handlers.deployments.deployments import Deployments
from SlashAPI.components.client.client import Connection
from SlashAPI.components.models.organization import organization_model

__all__ = ['OrganizationsHandler']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Production"


def validate_create_resp_details(response_data, name):
    """
    Method to validate if organization is created.
    :param response_data:
    :param name:
    :return:
    """
    assert_equal(response_data.json()['data']['createOrganization']['name'], name)
    assert_equal(response_data.json()['data']['createOrganization']['__typename'], "Organization")


def validate_get_organizations(response_data, name):
    """
    Method to validate get organization response.
    :param response_data:
    :param name:
    :return:
    """
    assert_equal(response_data.json()['data']['createOrganization']['name'], name)
    assert_equal(response_data.json()['data']['createOrganization']['__typename'], "Organization")


class OrganizationsHandler:
    """
        Class to handle organization methods
    """

    def __init__(self):
        self.header = None
        self.session_alias = "org_session"
        self.url = ""
        self.headers = {}
        self.connection = Connection()

    def create_session(self, headers, url, session_alias=None):
        """
        Method to set connection for organization
        :param session_alias:
        :param auth:
        :param url:
        :return:
        """
        if session_alias is not None:
            self.session_alias = session_alias
        self.headers = headers
        self.url = url
        self.connection.create_session(self.session_alias, self.url, headers=self.headers)
        logger.info("Created session as: " + self.session_alias + " organization request. ")
        return self.connection

    def create_organization(self, organization_name, expected_response=200, appender=None):
        """
        Method to create organizations
        :param appender:
        :param organization_name:
        :param expected_response:
        :return:
        """
        if appender is None:
            appender = "graphql"

        create_org_payload = organization_model.create_organization(organization_name)
        logger.debug(create_org_payload)
        response = self.connection.post_on_session(self.session_alias, appender, json=create_org_payload,
                                                   headers=self.headers, expected_status=str(expected_response))
        self.connection.request_should_be_successful(response)
        validate_create_resp_details(response, organization_name)

        return response.json()

    def delete_organization(self):
        """
        Method yet to be implemented.
        :param session_alias:
        :param expected_response:
        :return:
        """
        response = self.connection.delete_on_session(self.session_alias, "", headers=self.header)
        logger.info(response.json)

    def get_organizations(self, appender=None, expected_response=200):
        """
        Method to get the organization
        :param appender:
        :param expected_response:
        :return:
        """
        if appender is None:
            appender = "graphql"
        get_org_payload = organization_model.get_organization()
        logger.debug(get_org_payload)
        response = self.connection.post_on_session(self.session_alias, appender, json=get_org_payload,
                                                   headers=self.headers, expected_status=str(expected_response))
        self.connection.request_should_be_successful(response)
        return response

    def get_members_in_organization(self, appender=None, expected_response=200):
        """
        Method to get members for all the organizations
        :param expected_response:
        :param appender:
        :return:
        """
        if appender is None:
            appender = "graphql"
        existing_org_res = self.connection.post_on_session(self.session_alias, appender,
                                                           json=organization_model.get_members_in_organization(),
                                                           headers=self.headers, expected_status=str(expected_response))
        self.connection.request_should_be_successful(existing_org_res)
    
    def get_members_from_organization(self, org_uid, expected_response_text, expected_response=200, appender=None):
        """
        Method to get members from organization
        :param organization_uid
        :param expected_response:
        :param appender:
        :return:
        """
        if appender is None:
            appender = "graphql"
        get_org_members = organization_model.get_members_in_organization(org_uid)
        logger.debug(get_org_members)
        existing_org_res = self.connection.post_on_session(self.session_alias, appender, json=get_org_members,
                                                           headers=self.headers, expected_status=str(expected_response))
        if "errors" in existing_org_res.json():
            if existing_org_res.json()["errors"][0]["message"] == expected_response_text:
                logger.info("Organization is not found")
        return existing_org_res.json()

    def get_member_uid_from_organization(self, member_email, expected_response=200, appender=None):
        """
        Method to get member uid from organization
        :param expected_response:
        :param appender:
        :param member_email:
        :return:
        """
        if appender is None:
            appender = "graphql"

        existing_org_res = self.connection.post_on_session(self.session_alias, appender,
                                                           json=organization_model.get_members_in_organization(),
                                                           headers=self.headers, expected_status=str(expected_response))
        member_uid = None
        for org in existing_org_res.json()["data"]["organizations"]:
            for member in org["members"]:
                if member["auth0User"]["email"] == member_email:
                    member_uid = member["uid"]
        if member_uid is None:
            raise Exception("Member not found in organization: " + member_email)
        return member_uid

    def add_member_to_organization(self, org_uid, member_email, expected_response_text="OK", expected_response=200, appender=None):
        if appender is None:
            appender = "graphql"

        # add member to org req
        add_mem_payload = organization_model.add_member_to_organization(member_email, org_uid)
        logger.debug(add_mem_payload)

        response = self.connection.post_on_session(self.session_alias, appender,
                                                    json=add_mem_payload,
                                                    headers=self.headers, expected_status=str(expected_response))
        if "errors" in response.json():
            if response.json()["errors"][0]["message"] == expected_response_text:
                logger.info("Organization is not found")
        return response.json()

    def check_member_in_organization(self, org_uid, member_email, expected_response=200, appender=None):
        """
        Method to add a member to organization
        :param appender:
        :param expected_response:
        :param org_uid: <existing_org_uid>
        :param member_email: <new member mail>
        :return:<response>
        """

        if appender is None:
            appender = "graphql"

        # add member to org req
        add_mem_payload = organization_model.add_member_to_organization(member_email, org_uid)
        logger.debug(add_mem_payload)

        response = self.connection.post_on_session(self.session_alias, appender,
                                                    json=add_mem_payload,
                                                    headers=self.headers, expected_status=str(expected_response))
        self.connection.request_should_be_successful(response)

        check = False
        if "errors" in response.json():
            if response.json()["errors"][0]["message"] == "The user is already a part of the organization.":
                logger.info("User already exists..")
                check = True
        return check

    def remove_member_from_organization(self, org_uid, member_email, expected_response=200, appender=None):
        """
        Method to delete a member from organization
        :param appender:
        :param org_uid: <existing_org_uid>
        :param member_email: <new member mail>
        :param expected_response:
        :return:<response>
        """

        if appender is None:
            appender = "graphql"

        member_uid = self.get_member_uid_from_organization(member_email)
        logger.debug(member_uid)

        # remove member from org request
        del_mem_payload = organization_model.del_member_from_organization(member_uid, org_uid)
        logger.debug(del_mem_payload)

        if member_uid:
            response = self.connection.post_on_session(self.session_alias, appender,
                                                       json=del_mem_payload,
                                                       headers=self.headers, expected_status=str(expected_response))
            self.connection.request_should_be_successful(response)
            if "errors" in response.json():
                if "The user is already a part of the organization." in response.json():
                    raise Exception("User does not exists.." + member_email)
        else:
            raise Exception("Member is not found: " + member_uid)

        return response.json()

    def remove_org_from_deployment(self, deployment_name, expected_response=200):
        """
        Method to remove organization from deployment
        :param expected_response:
        :param deployment_name:
        :return:
        """
        deployment_handler = Deployments()
        session_alias = "remove_dep"
        dep_data = deployment_handler.get_deployments(session_alias, self.url+"/deployments", self.headers, expected_response)
        logger.debug(dep_data)
        dep_uid = None
        for dep_res in dep_data:
            if dep_res["name"] == deployment_name:
                dep_uid = dep_res["uid"]
        logger.debug(dep_uid)
        if dep_uid is None:
            raise Exception("Exception occurred while removing deployment from organization"
                            ", deployment was not found: " + deployment_name)

        response = deployment_handler.update_deployment(session_alias, self.url+"/deployment/" + str(dep_uid),
                                                        organizationId="empty", auth=self.headers, expected_response=str(expected_response))
        return response

    def add_org_from_deployment(self, deployment_name, org_uid, expected_response=200):
        """
        Method to add organization to deployment
        :param expected_response:
        :param deployment_name:
        :param org_uid:
        :return:
        """
        logger.info(deployment_name)
        deployment_handler = Deployments()
        session_alias = "add_dep"
        dep_data = deployment_handler.get_deployments(session_alias, self.url+"/deployments", self.headers, expected_response)
        logger.debug(dep_data)
        dep_uid = None
        for dep_res in dep_data:
            if dep_res["name"] == deployment_name:
                dep_uid = dep_res["uid"]
        logger.debug(dep_uid)
        logger.debug(deployment_name)
        if dep_uid is None:
            raise Exception("Exception occurred while removing deployment from organization"
                            ", deployment not found: " + deployment_name)
        response = deployment_handler.update_deployment(session_alias, self.url+"/deployment/" + dep_uid,
                                                        organizationId=org_uid, auth=self.headers, expected_response=str(expected_response))
        logger.debug(response.json())
        response.json()["org_uid"] = org_uid
        return response.json()
