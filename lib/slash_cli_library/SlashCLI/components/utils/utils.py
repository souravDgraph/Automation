# !/usr/bin/env python
# coding=utf-8
# pylint: disable=too-many-arguments, missing-function-docstring, unused-argument, too-many-locals, invalid-name
"""
Author: vivetha@dgraph.io
"""
import subprocess
from robot.api import logger

__all__ = ['Utils']
__author__ = "Vivetha Madesh"
__version__ = "1.0"
__maintainer__ = "Vivetha Madesh"
__email__ = "vivetha@dgraph.io"
__status__ = "Production"


class Utils:

    """
    Defines handlers for Deployment related end points

    """
    @staticmethod
    def execute_slash_graphql_command(command,
                                      options,
                                      expected_returncode=0):
        slash_command = "slash-graphql " + command + options
        output = subprocess.Popen(slash_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, error = output.communicate()
        logger.info("-.-."*30)
        logger.info("Command Executed is : %s" % slash_command)
        logger.info("Command return code is : %s " % str(output.returncode))
        logger.info("Command output is : %s " % str(stdout))
        logger.info("Error statement is : %s " % str(error))
        logger.info("-.-." * 30)
        if str(output.returncode) != str(expected_returncode):
            logger.info("Expected Return code : %s " % str(output.returncode))
            logger.info("Actual return code: %s " % str(expected_returncode))
            raise Exception("Expected return code not Found !!!!")
        return str(stdout), str(error)


