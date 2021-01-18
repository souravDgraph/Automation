"""
Custom Request Library for Dgraph
"""
__all__ = ['CustomRequestKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"

import json
from robot.api import logger
from Dgraph.components.request_handler import RequestHandler
from Dgraph.components.setup_configurations import DgraphCLI

# pylint: disable=R0912
# pylint: disable=R0915



class CustomRequestKeywords:
    """
    Custom Request Keywords Class.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = __version__

    ROBOT_CODE_ROOT_FOLDER_PATH = None
    ROBOT_CODE_BRANCH_FOLDER_PATH = None
    ROBOT_CODE_UTILS_FOLDER_PATH = None
    OS = None

    def __init__(self):
        self.req_handler: RequestHandler = RequestHandler("")
        self.dgraph_cli: DgraphCLI = DgraphCLI()

    def connect_request_server(self, url):
        """
        Method to connect to url to perform backup.
        :param url:
        :return: the instance of RequestHandler object
        """
        self.req_handler = RequestHandler(url)
        self.dgraph_cli = DgraphCLI()
        logger.info("Requested URL:" + url)

    def post_nfs_backup_restore_command(self, appender, path, req_type: str):
        """
        Method to post dgraph backup | restore  nfs request and validate the response.
        \n:param appender: /admin || /admin/backup
        \n:param path: path to the backup folder in the local.
        \n:param req_type: <post type> | backup || restore
        \n:return: <response>

        Example:
        | Post Nfs backup restore Command | /admin | /path/backup | backup
        | Post Nfs backup restore Command | /admin/backup | /path/backup | backup
        | Post Nfs backup restore Command | /admin | /path/backup | restore
        """

        login_response = ""
        awt_token = ""
        logger.info("backup path: " + path)
        logger.info("POST command has been requested for: " + appender)

        # Check the configurations
        if self.dgraph_cli.get_acl() and "https" in self.req_handler.url and appender == "/admin":
            login_body = "{\"query\":\"mutation {\\n    " \
                         "login(userId: \\\"groot\\\", " \
                         "password: \\\"password\\\") {\\n   " \
                         "         response {\\n                        " \
                         "accessJWT\\n                        " \
                         "refreshJWT\\n                   " \
                         " }\\n    }\\n}\",\"variables\":{}} "
            cert = ""
            if self.dgraph_cli.get_tls():
                tls_cert = self.dgraph_cli.curr_path + \
                           self.dgraph_cli.cfg['tls']['location'] + "/ca.crt"
                cert = tls_cert
            headers = {
                'Content-Type': 'application/json'
            }
            # Generating awt_token
            login_response = self.req_handler.post_request(appender, headers, login_body, cert)
            awt_token = login_response.json()['data']['login']['response']['accessJWT']
        elif self.dgraph_cli.get_acl():
            raise Exception("Use https request to proceed with the post call "
                            "since ACL is enabled or check if it's requested only "
                            "for /admin call .\n url requested: "
                            + self.req_handler.url + " appender's used: " + appender)

        # Post call for /admin request
        if appender == "/admin":
            payload = ""
            if req_type.lower() == "backup":
                payload = "{\"query\":\"mutation {\\n  backup(input: {destination: " \
                          "\\\"" + path + "\\\"}) {\\n    " \
                                          "response {\\n      message\\n     " \
                                          " code\\n    }\\n  }\\n}\\n\",\"variables\":{" \
                                          "}} "
            elif req_type.lower() == "restore":
                payload = "{\"query\":\"mutation {\\n  restore(input: {location: " \
                          "\\\"" + path + "\\\"}) " \
                                          " {\\n      message\\n      code\\n    }" \
                                          "\\n}\\n\",\"variables\":{" \
                                          "}} "

            post_res = ""
            headers = {}
            if self.dgraph_cli.get_acl():
                logger.info(awt_token)
                headers = {
                    'X-Dgraph-AccessToken': awt_token,
                    'Content-Type': 'application/json'
                }
                post_res = self.req_handler.post_request(appender, headers, payload, cert)
            else:
                headers = {
                    'Content-Type': 'application/json'
                }
                post_res = self.req_handler.post_backup_request(appender, headers, payload)
            logger.info("After hitting the request\n" + json.dumps(post_res.json()))

        # Post call for /admin/backup request
        elif appender == "/admin/backup":
            payload = ""
            post_res = ""
            headers = {}
            if req_type.lower() == "backup":
                payload = {'destination': path}
            elif req_type.lower() == "restore":
                payload = {'location': path}
            if self.dgraph_cli.get_acl():
                logger.info(awt_token)
                headers = {'X-Dgraph-AccessToken': awt_token}
                post_res = self.req_handler.post_request(appender, headers, payload, cert)
            else:
                post_res = self.req_handler.post_backup_request(appender, headers, payload)
            logger.info("After hitting the request\n" + json.dumps(post_res.json()))

        # Validations for the output generated for backup | restore
        try:
            if req_type.lower() == "backup":
                if post_res.json()['data']['backup']['response']['code'] == 'Success' and \
                        post_res.json()['data']['backup']['response']['message'] \
                        == 'Backup completed.':
                    logger.info('Backup successfully completed')
            elif req_type.lower() == "restore":
                if post_res.json()['data']['restore']['code'] == 'Success' and \
                        post_res.json()['data']['restore']['message'] == \
                        'Restore operation started.':
                    logger.info('Restore successfully completed')
        except Exception as err:
            raise Exception("Something went wrong with the data params.."
                            + json.dumps(post_res.json())) from err

        return post_res

    def get_command(self):
        """
        Method to perform a get request for the dgraph.
        \n:return: response
        """
        logger.info("Hitting the get method.")
        get_res = self.req_handler.get_request()
        return get_res

    def get_command_with_appender(self, appender):
        """
        Method to perform a get request for any appender provided.
        \n:param appender: /*
        \n:return: response
        """
        logger.info("Hitting the get method with appender")
        logger.info("appending: " + appender + " to url")
        get_res = self.req_handler.get_request_appender(appender)
        return get_res
