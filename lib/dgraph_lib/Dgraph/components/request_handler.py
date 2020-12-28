"""
 Custom request class for Request Calls
"""
import json
import requests
from requests import RequestException, Response
from robot.api import logger
# pylint: disable=E1121

__all__ = ['RequestHandler']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"


class RequestHandler:
    """
    Handles all the request calls customized as per Dgraph
    """

    def __init__(self, url):
        self.url = url
        self.headers = {}

    def post_request(self, appender, headers, body, cert):
        """
        Method to perform a basic POST call and return the response

        :param appender: url appender's
        :param headers: any headers {}
        :param body: post body
        :param cert: certificates
        :return:<response>
        """
        logger.debug("inside post_request --> ")
        response = Response()
        try:
            response = requests.post(self.url + appender, headers=headers, data=body,  verify=cert)
            if "errors" in response.json():
                raise Exception("Post Request failed:\n" + json.dumps(response.json()))
        except RequestException as res_error:
            logger.warn(res_error, response.text, response.status_code)
        logger.debug(response.json())
        return response

    def post_backup_request(self, appender, headers, body):
        """
        Method to request a post call for the provided appender and body.
        :param appender: /admin || /admin/backup
        :param headers: any headers {}
        :param body: params
        :return: response
        """

        logger.info("Hitting post request at: "+self.url + appender)
        self.headers = headers
        response = Response()
        try:
            response = requests.request("POST", self.url + appender, headers=headers, data=body)
            if "errors" in response.json():
                raise Exception("Post Request failed:\n" + json.dumps(response.json()))
        except RequestException as res_error:
            logger.warn(res_error, response.text, response.status_code)
        return response

    def get_request(self):
        """
        Method yet to implement..
        :return: response
        """
        response = requests.get(self.url)
        logger.info(response.text)
        return response

    def get_request_appender(self, appender):
        """
        Method to perform the get request for a provided appender
        :param appender: /*
        :return: response
        """
        logger.info("Hitting get request at: " + self.url+appender)
        response = requests.get(self.url+appender)
        logger.info(response.text)
        return response
