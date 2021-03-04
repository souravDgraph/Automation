# !/usr/bin/env python
# coding=utf-8

from robot.api import logger
from SlashCLI.components.utils.utils import Utils

__all__ = ['Organizations']
__author__ = "Santhosh Sekar"
__version__ = "1.0"
__maintainer__ = "Santhosh Sekar"
__email__ = "santhosh@dgraph.io"
__status__ = "Production"

class Organizations:

    @staticmethod
    def get_organizations(environment, quiet=None, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["expected_return_code"]
        base_command = "list-organizations"
        options = ""
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
<<<<<<< HEAD
                logger.info(properties[key])
=======
                logger.info(type(key))
                logger.info(properties[key])
                logger.info(type(options))
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
                options += " --" + key + "=" + properties[key]

        logger.info(base_command)
        logger.info(options)
        output, error = Utils.execute_slash_graphql_command(base_command, 
                                                            options, 
                                                            expected_return_code)
        logger.info(error)
        return output
    
    @staticmethod
    def get_organization_id(environment, org_name, expected_return_code=0):
        organization_details = Organizations.get_organizations(environment, expected_return_code)
        organizations = organization_details.split("\\n")
        for organization in organizations:
            if org_name in organization:
                logger.info(organization)
                organization_details = organization.split(" ")
                org_uid = organization_details[0]
                logger.info(org_uid)
        return org_uid

    @staticmethod
<<<<<<< HEAD
    def create_organization(environment, org_name, expected_output_text, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["org_name", "expected_output_text", "expected_return_code"]
=======
    def create_organization(environment, org_name, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["org_name","expected_return_code"]
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
        base_command = "create-organization "
        options = org_name
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
<<<<<<< HEAD
                logger.info(properties[key])
=======
                logger.info(type(key))
                logger.info(properties[key])
                logger.info(type(options))
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
                options += " --" + key + "=" + properties[key]

        logger.info(base_command)
        logger.info(options)
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
<<<<<<< HEAD
        if expected_output_text not in str(output) and expected_return_code==0:
            raise Exception("Unble to create organization")
=======
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
        logger.info(error)
        return output

    @staticmethod
<<<<<<< HEAD
    def add_member_to_organization(environment, org_uid, member_email, expected_output_text, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["org_uid", "member_email", "expected_return_code", "expected_output_text"]
=======
    def add_member_to_organization(environment, org_uid, member_email, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["org_uid", "member_email", "expected_return_code"]
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
        base_command = "add-member-to-organization "
        options = org_uid + " " + member_email
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
<<<<<<< HEAD
                logger.info(properties[key])
=======
                logger.info(type(key))
                logger.info(properties[key])
                logger.info(type(options))
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
                options += " --" + key + "=" + properties[key]

        logger.info(base_command)
        logger.info(options)
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
<<<<<<< HEAD
        if expected_output_text not in str(output) and expected_return_code==0:
            raise Exception("Unable to add member to organization")
        elif expected_output_text not in str(error) and expected_return_code!=0:
            raise Exception("Expected error message is not found")
=======
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
        logger.info(error)
        return output

    @staticmethod
<<<<<<< HEAD
    def remove_member_from_organization(environment, org_uid, member_email, expected_output_text, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["org_uid", "member_email", "expected_output_text", "expected_return_code"]
=======
    def remove_member_from_organization(environment, org_uid, member_email, expected_return_code=0):
        properties = locals()
        properties_to_exclude = ["org_uid", "member_email", "expected_return_code"]
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
        base_command = "remove-member-from-organization "
        options = org_uid + " " + member_email
        for key in properties.keys():
            if properties[key] and key not in properties_to_exclude:
<<<<<<< HEAD
                logger.info(properties[key])
=======
                logger.info(type(key))
                logger.info(properties[key])
                logger.info(type(options))
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
                options += " --" + key + "=" + properties[key]

        logger.info(base_command)
        logger.info(options)
        output, error = Utils.execute_slash_graphql_command(base_command,
                                                            options,
                                                            expected_return_code)
<<<<<<< HEAD
        if expected_output_text not in str(output) and expected_return_code==0:
            raise Exception("Unable to remove member from organization")
        elif expected_output_text not in str(error) and expected_return_code!=0:
            raise Exception("Expected error message is not found")
=======
>>>>>>> 9d18ce9bb68a318b7a0d1a8ac9e6e8d441614002
        logger.info(error)
        return output
