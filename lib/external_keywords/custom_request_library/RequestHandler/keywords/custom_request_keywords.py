__all__ = ['CustomRequestKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "tkrishnakaushik96@gmail.com"
__status__ = "Stagging"

from RequestHandler.components.request_handler import RequestHandler
from robot.api import ResultWriter
from robot.api import logger
import json


class CustomRequestKeywords:
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    ROBOT_CODE_ROOT_FOLDER_PATH = None
    ROBOT_CODE_BRANCH_FOLDER_PATH = None
    ROBOT_CODE_UTILS_FOLDER_PATH = None
    OS = None

    def connect_server(self, url):
        self.req_handler = RequestHandler(url)

    def post_nfs_command(self, appender, path):

        logger.info("backup path: " + path)
        logger.info("POST command has been requested for: " + appender)
        # payload = {'destination': '/Users/apple/Desktop/Dgraph_workspace/robot_framework/dgraph_framework/backup'}
        if appender == "/admin":
            payload = "{\"query\":\"mutation {\\n  backup(input: {destination: " \
                      "\\\"" + path + "\\\"}) {\\n    " \
                                      "response {\\n      message\\n      code\\n    }\\n  }\\n}\\n\",\"variables\":{" \
                                      "}} "
            post_res = self.req_handler.post_request(appender, payload)
            logger.info("After hitting the request\n" + json.dumps(post_res.json()))

        elif appender == "/admin/backup":
            payload = {'destination': path}
            post_res = self.req_handler.post_request(appender, payload)
            logger.info("After hitting the request\n"+json.dumps(post_res.json()))
        try:
            if post_res.json()['data']['backup']['response']['code'] == 'Success' and post_res.json()['data']['backup']['response']['message'] == 'Backup completed.':
                logger.info('Backup sucessfully completed')
        except Exception as err:
            raise Exception("Something went wrong with the data params.." + json.dumps(post_res.json()))

        return post_res

    def get_command(self):
        logger.info("Hitting the get method.")
        get_res = self.req_handler.get_request()
        return get_res

    def get_command(self, appender):
        logger.info("Hitting the get method with appender")
        logger.info("appending: " + appender + " to url")
        get_res = self.req_handler.get_request(appender)
        return get_res
