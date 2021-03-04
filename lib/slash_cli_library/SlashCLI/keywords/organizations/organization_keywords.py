# !/usr/bin/env python
# coding=utf-8

from robot.api import logger
from SlashCLI.components.organizations.organizations import Organizations

__all__ = ['OrganizationKeywords']
__author__ = "Santhosh Sekar"
__version__ = "1.0"
__maintainer__ = "Santhosh Sekar"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"


class OrganizationKeywords:

    @staticmethod
    def get_organizations(environment):
        logger.info("Get all organizations")
        organizations = Organizations.get_organizations(environment)
        return organizations

    @staticmethod
    def create_organization(environment, org_name, expected_output_text=None, expected_return_code=0):
        logger.info("Creating Organization")
        organization = Organizations.create_organization(environment,
                                                            org_name,
                                                            expected_output_text,
                                                            expected_return_code)
        return organization

    @staticmethod
    def add_member_to_organization(environment, org_uid, member_email, expected_output_text=None, expected_return_code=0):
        logger.info("Adding a member to an organization")
        org_member = Organizations.add_member_to_organization(environment,
                                                                org_uid,
                                                                member_email,
                                                                expected_output_text,
                                                                expected_return_code)
        return  org_member

    @staticmethod
    def get_organization_id(environment, organization, expected_return_code=0):
        logger.info("Getting Organization ID")
        org_uid = Organizations.get_organization_id(environment,
                                                        organization,
                                                        expected_return_code)
        return org_uid

    @staticmethod
    def remove_member_from_organization(environment, org_uid, member_email, expected_output_text=None, expected_return_code=0):
        logger.info("Removing a member from an organization")
        Organizations.remove_member_from_organization(environment, 
                                                        org_uid,
                                                        member_email,
                                                        expected_output_text,
                                                        expected_return_code)
                                