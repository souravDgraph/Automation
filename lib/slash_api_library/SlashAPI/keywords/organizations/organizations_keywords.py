# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, W0201, C0301
"""
Author: krishna@dgraph.io
"""

from robot.api import logger
from SlashAPI.components.handlers.organizations.organizations_handler import OrganizationsHandler

__all__ = ['OrganizationsKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Production"


class OrganizationsKeywords:
    """

    Main organizations:
    - Create Session for Organization should be initialized before working on request.

    """

    def create_session_for_organization(self, headers, url, session_alias=None):
        """
        Method to create session for organizations
        \n:param session_alias: <name for the session>
        \n:param auth:<bearer type auth code>
        \n:param url: <URL>
        \n:return:<response>

        Example:
        | create session for organization | headers | url | session_alias <optional>
        """
        self.org_handler = OrganizationsHandler()
        logger.info("Creating a session for Organization")
        if session_alias:
            res = self.org_handler.create_session(headers=headers, url=url, session_alias=session_alias)
        else:
            res = self.org_handler.create_session(headers=headers, url=url)
        return res

    def create_organization(self, org_name, expected_response=200, appender=None):
        """
        Method to create organization.
        \n:param org_name: <organization_name>
        \n:param expected_response: <status_code>
        \n:param appender:
        \n:return:<response>

        Example:
        | create organization | org_name | expected_response=200
        | create organization | dgraph_org | expected_response=200
        """
        logger.info("Creating organization for: " + org_name)
        if appender is None:
            return self.org_handler.create_organization(organization_name=org_name,
                                                 expected_response=expected_response)
        else:
            return self.org_handler.create_organization(organization_name=org_name,
                                                 expected_response=expected_response,
                                                 appender=appender)

    def get_organizations_list(self):
        """
        Method to get all the organizations as part of the client.
        \n:param expected_response: <status_code>
        \n:return:<response>

        Example:
        | get organizations list |
        """
        logger.info("Getting lis of organizations for the client.")
        return self.org_handler.get_organizations()

    def get_members_from_organization(self, org_uid, expected_response_text="OK", appender=None, expected_response=200):
        # Method to get the members from organization with organization uid
        if appender is None:
            response = self.org_handler.get_members_from_organization(org_uid, expected_response_text, expected_response)
        else:
            response = self.org_handler.get_members_from_organization(org_uid, expected_response_text, expected_response, appender=appender)

        return response

    def add_new_member_to_existing_organization(self, org_uid, member_email, expected_response_text="OK", appender=None):
        # Method to add a member to an organization with organization uid and member email id
        if appender is None:
            response = self.org_handler.add_member_to_organization(org_uid, member_email, expected_response_text)
        else:
            response = self.org_handler.add_member_to_organization(org_uid, member_email, expected_response_text,
                                                            appender=appender)
        return response

    def check_if_member_is_already_existing_in_organization(self, org_uid, member_email):
        """
        Method to check a member to existing organization
        \n:param org_uid:<existing_organization_uid>
        \n:param member_email:<new_member_email-id>
        \n:return: isExisting <boolean>

        Example:
        | add new member to existing organization |  org_uid | member_email
        | add new member to existing organization |  0x202ef | tester@gmail.com
        """
        return self.org_handler.check_member_in_organization(org_uid, member_email)

    def remove_member_from_existing_organization(self, org_uid, member_email, appender=None):
        """
        Method to remove a member from organization
        :param appender: <if needed for url>
        :param org_uid: <organization_uid>
        :param member_email: <email_id>
        :return: <json_response>

        Example:
        | remove member from existing organization |  org_uid | member_email | appender <optional>
        | remove member from existing organization |  0x201ef | tester@gmail.com |
        """
        if appender:
            response = self.org_handler.remove_member_from_organization(org_uid, member_email, appender)
        else:
            response = self.org_handler.remove_member_from_organization(org_uid, member_email)
        return response

    def remove_org_from_deployment(self, deployment_name):
        """
        Method to remove organization from deployment
        :param deployment_name:
        :return: <response>

        Example:
        | remove org from deployment |  deployment_name |
        | remove org from deployment |  backend_deployment_name |
        | remove org from deployment |  Pokemon |
        """
        return self.org_handler.remove_org_from_deployment(deployment_name)

    def add_org_to_deployment(self, deployment_name, org_uid):
        """
        Method to remove organization from deployment
        :param deployment_name: <deployment_name>
        :param org_uid: <organization_uid>
        :return: response

        Example:
        | add org to deployment |  deployment_name | org_uid |
        | add org to deployment |  Pokemon | 0x201ef |
        """
        return self.org_handler.add_organization_to_deployment(deployment_name, org_uid)
