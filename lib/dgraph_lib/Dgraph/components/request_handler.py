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

    def post_request(self, appender, headers, body, cert=None):
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
            if cert is None:
                response = requests.post(self.url + appender, headers=headers, data=body)
            else:
                response = requests.post(self.url + appender, headers=headers, data=body, verify=cert)
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

    def post(self, appender, headers, query, variables=None, cert=None):
        """
        Method to perform a basic POST call and return the response

        :param appender: url appender's
        :param headers: any headers {}
        :param query: graphQL Query
        :param variables: graphQL variables
        :param cert: certificates
        :return:<response>
        """
        if variables is None:
            variables = {}
        logger.debug("inside post_request --> ")
        response = Response()
        try:
            if cert is None:
                response = requests.post(self.url + appender, headers=headers,
                                         json={'query': query, 'variables': variables})
            else:
                response = requests.post(self.url + appender, headers=headers,
                                         json={'query': query, 'variables': variables},  verify=cert)
            if "errors" in response.json():
                raise Exception(f"POST Request failed:\n {json.dumps(response.json())}")
        except RequestException as res_error:
            logger.warn(res_error, response.text)
        logger.debug(response.json())
        return response

    def get(self, appender, headers, parameters=None, cert=None):
        """
        Method to perform the get request for a provided appender
        :param appender: /*
        :param headers:
        :param parameters:
        :param cert:
        :return: response
        """
        if parameters is None:
            parameters = {}
        logger.info("Hitting get request at: " + self.url + appender)
        response = Response()
        try:
            if cert is None:
                response = requests.get(f"{self.url}{appender}", headers=headers, params=parameters)
            else:
                response = requests.get(f"{self.url}{appender}", headers=headers, params=parameters, verify=cert)
            if "errors" in response.json():
                raise Exception(f"GET Request failed:\n {json.dumps(response.json())}")
        except RequestException as res_error:
            logger.warn(res_error, response.text)
        logger.debug(response.json())
        return response
