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
from robot.utils.asserts import assert_equal
from Dgraph.components.request_handler import RequestHandler
from Dgraph.components.setup_configurations import DgraphCLI
from Dgraph.keywords import constants


# pylint: disable=R0912
# pylint: disable=R0915


class CustomRequestKeywords:
    """
    Custom Request Keywords Class.
    """

    def connect_request_server(self, url=None):
        """
        Method to connect to url to perform backup.
        :param url:
        :return: the instance of RequestHandler object
        """
        self.headers = constants.COMMON_HEADER
        self.dgraph_cli = DgraphCLI()
        self.cert = None
        if url is not None:
            self.req_handler = RequestHandler(url)
        else:
            if self.dgraph_cli.get_tls():
                url = "https://localhost:8080"
            else:
                url = "http://localhost:8080"
            self.req_handler = RequestHandler(url)

        logger.info("Requested URL: " + url)

        if self.dgraph_cli.get_tls():
            self.cert = self.get_certs()
            logger.info("TLS is configured.")
        if self.dgraph_cli.get_acl():
            self.headers = self.login('/admin')

    # def post_nfs_backup_restore_command(self, appender, path, req_type: str):
    #     """
    #     Method to post dgraph backup | restore  nfs request and validate the response.
    #     \n:param appender: /admin || /admin/backup
    #     \n:param path: path to the backup folder in the local.
    #     \n:param req_type: <post type> | backup || restore
    #     \n:return: <response>
    #
    #     Example:
    #     | Post Nfs backup restore Command | /admin | /path/backup | backup
    #     | Post Nfs backup restore Command | /admin/backup | /path/backup | backup
    #     | Post Nfs backup restore Command | /admin | /path/backup | restore
    #     """
    #
    #     login_response = ""
    #     awt_token = ""
    #     logger.info("backup path: " + path)
    #     logger.info("POST command has been requested for: " + appender)
    #
    #     # Check the configurations
    #     if self.dgraph_cli.get_acl() and "https" in self.req_handler.url and appender == "/admin":
    #         login_body = "{\"query\":\"mutation {\\n    " \
    #                      "login(userId: \\\"groot\\\", " \
    #                      "password: \\\"password\\\") {\\n   " \
    #                      "         response {\\n                        " \
    #                      "accessJWT\\n                        " \
    #                      "refreshJWT\\n                   " \
    #                      " }\\n    }\\n}\",\"variables\":{}} "
    #         cert = ""
    #         if self.dgraph_cli.get_tls():
    #             tls_cert = self.dgraph_cli.curr_path + \
    #                        self.dgraph_cli.cfg['tls']['location'] + "/ca.crt"
    #             cert = tls_cert
    #         headers = {
    #             'Content-Type': 'application/json'
    #         }
    #         # Generating awt_token
    #         login_response = self.req_handler.post_request(appender, headers, login_body, cert)
    #         awt_token = login_response.json()['data']['login']['response']['accessJWT']
    #     elif self.dgraph_cli.get_acl():
    #         raise Exception("Use https request to proceed with the post call "
    #                         "since ACL is enabled or check if it's requested only "
    #                         "for /admin call .\n url requested: "
    #                         + self.req_handler.url + " appender's used: " + appender)
    #
    #     # Post call for /admin request
    #     if appender == "/admin":
    #         payload = ""
    #         if req_type.lower() == "backup":
    #             payload = "{\"query\":\"mutation {\\n  backup(input: {destination: " \
    #                       "\\\"" + path + "\\\"}) {\\n    " \
    #                                       "response {\\n      message\\n     " \
    #                                       " code\\n    }\\n  }\\n}\\n\",\"variables\":{" \
    #                                       "}} "
    #         elif req_type.lower() == "restore":
    #             payload = "{\"query\":\"mutation {\\n  restore(input: {location: " \
    #                       "\\\"" + path + "\\\"}) " \
    #                                       " {\\n      message\\n      code\\n    }" \
    #                                       "\\n}\\n\",\"variables\":{" \
    #                                       "}} "
    #
    #         post_res = ""
    #         headers = {}
    #         if self.dgraph_cli.get_acl():
    #             logger.info(awt_token)
    #             headers = {
    #                 'X-Dgraph-AccessToken': awt_token,
    #                 'Content-Type': 'application/json'
    #             }
    #             post_res = self.req_handler.post_request(appender, headers, payload, cert)
    #         else:
    #             headers = {
    #                 'Content-Type': 'application/json'
    #             }
    #             post_res = self.req_handler.post_backup_request(appender, headers, payload)
    #         logger.info("After hitting the request\n" + json.dumps(post_res.json()))
    #
    #     # Post call for /admin/backup request
    #     elif appender == "/admin/backup":
    #         payload = ""
    #         post_res = ""
    #         headers = {}
    #         if req_type.lower() == "backup":
    #             payload = {'destination': path}
    #         elif req_type.lower() == "restore":
    #             payload = {'location': path}
    #         if self.dgraph_cli.get_acl():
    #             logger.info(awt_token)
    #             headers = {'X-Dgraph-AccessToken': awt_token}
    #             post_res = self.req_handler.post_request(appender, headers, payload, cert)
    #         else:
    #             post_res = self.req_handler.post_backup_request(appender, headers, payload)
    #         logger.info("After hitting the request\n" + json.dumps(post_res.json()))
    #
    #     # Validations for the output generated for backup | restore
    #     try:
    #         if req_type.lower() == "backup":
    #             if 'Success' in post_res.json() and \
    #                'Backup completed.' in  post_res.json():
    #                 logger.info('Backup successfully completed')
    #         elif req_type.lower() == "restore":
    #             if post_res.json()['data']['restore']['code'] == 'Success' and \
    #                     post_res.json()['data']['restore']['message'] == \
    #                     'Restore operation started.':
    #                 logger.info('Restore successfully completed')
    #     except Exception as err:
    #         raise Exception("Something went wrong with the data params.."
    #                         + json.dumps(post_res.json())) from err
    #
    #     return post_res

    def login(self, appender):
        """
        Method to Login to the dgraph server and generate the jwt token
        :param appender: URL segment to append to the base URL
        """
        query = constants.LOGIN_BODY
        variables = None
        login_response = self.req_handler.post(appender=appender, headers=self.headers, query=query,
                                               variables=variables, cert=self.cert)
        jwt_token = login_response.json()['data']['login']['response']['accessJWT']
        return_header = {
            'X-Dgraph-AccessToken': jwt_token,
            'Content-Type': 'application/json'
        }
        logger.info("login Successful")
        return return_header

    def get_certs(self):
        """
        Method to get TLS certificates if required by the configuration
        """
        tls_cert = f"{self.dgraph_cli.curr_path}{self.dgraph_cli.cfg['tls']['location']}/ca.crt"
        return tls_cert

    def health_check(self, appender):
        """
        Method to check the health of the deployed dgraph instance
        :param appender: URL segment to add to the base URL
        :return status: healthy/unhealthy
        """
        cert = self.cert
        headers = self.headers
        response = None
        try:
            response = self.req_handler.get(appender=appender, headers=headers, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the data params.. {json.dumps(response.json())}") from err
        status = response.json()[0]['status']
        return status

    def state_check(self, appender):
        """
        Method to check the state of the deployed database instance
        :param appender: URL segment to add to the base URL
        :return state: Complete state of the database
        """
        cert = self.cert
        headers = self.headers
        response = None
        try:
            response = self.req_handler.get(appender=appender, headers=headers, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the data params.. {json.dumps(response.json())}") from err
        state = response.json()
        return state

    def remove_node(self, appender, alpha_id, group):
        """
        Method to remove alpha node from a cluster, this API sends the request on the zero port and removes a alpha node
        :param appender: URL segment to add to the base URL
        :param alpha_id: ID of the alpha in the cluster (can get this value from state check)
        :param group: group number in which the alpha belongs
        :return: <response>
        """
        cert = self.cert
        headers = self.headers
        parameters = {'id': alpha_id, 'group': group}
        response = None
        try:
            response = self.req_handler.get(appender=appender, headers=headers, parameters=parameters, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the data params.. {json.dumps(response.json())}") from err
        return response

    def backup_using_admin(self, path):
        """
        Method to call backup GraphQL mutation on dgraph, this will trigger a backup
        :param appender: URL segment to add to the base URL
        :param path: Backup path
        :return: <response>
        """
        cert = self.cert
        headers = self.headers
        query = constants.BACKUP_QUERY
        variables = {'path': path}
        response = None
        appender = "/admin"
        try:
            response = self.req_handler.post(appender=appender, headers=headers, query=query,
                                             variables=variables, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the backup request.. {json.dumps(response.json())}") from err
        assert_equal(response.json()['data']['backup']['response']['code'], 'Success')
        assert_equal(response.json()['data']['backup']['response']['message'], 'Backup completed.')
        logger.info('Backup successfully completed')
        return response

    def restore_using_admin(self, path):
        """
        Method to call restore GraphQL mutation on dgraph, this will trigger a restore
        :param appender: URL segment to add to the base URL
        :param path: Path to the restore manifest to trigger a restore
        :return: <response>
        """
        cert = self.cert
        headers = self.headers
        query = constants.RESTORE_QUERY
        variables = {'path': path}
        response = None
        appender = "/admin"

        try:
            response = self.req_handler.post(appender=appender, headers=headers, query=query,
                                             variables=variables, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the restore request.. {json.dumps(response.json())}") from err
        assert_equal(response.json()['data']['restore']['code'], 'Success')
        assert_equal(response.json()['data']['restore']['message'], 'Restore operation started.')
        logger.info('Restore successfully started')
        return response

    def backup_using_admin_backup(self, path):
        """
        Method to call backup using the /admin/backup API, this does not use a GraphQL request
        :param appender: URL segment to add to the base URL
        :param path: path to backup the database
        :return: <response>
        """
        cert = self.cert
        headers = self.headers
        payload = {'destination': path}
        response = None
        appender = "/admin/backup"
        try:
            response = self.req_handler.post_request(appender=appender, headers=headers, body=payload, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the backup request... {json.dumps(response.json())}") from err
        assert_equal(response.json()['data']['backup']['response']['code'], 'Success')
        assert_equal(response.json()['data']['backup']['response']['message'], 'Backup completed.')
        logger.info('Backup successfully completed')
        return response

    def restore_using_admin_backup(self, path):
        """
        Method to call a restore using the /admin/backup API, this does not use a GraphQL request
        :param appender: URL segment to add to the base URL
        :param path: Path to the restore manifest to the database for triggering restore
        :return: <response>
        """
        cert = self.cert
        headers = self.headers
        payload = {'location': path}
        response = None
        appender = "/admin/backup"
        try:
            response = self.req_handler.post_request(appender=appender, headers=headers, body=payload, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the restore request... {json.dumps(response.json())}") from err
        assert_equal(response.json()['data']['restore']['code'], 'Success')
        assert_equal(response.json()['data']['restore']['message'], 'Restore operation started.')
        logger.info('Restore successfully started')
        return response

    def export_data_admin(self, appender, data_format):
        """
        Method to export the database using the GraphQL export mutation
        :param appender: URL segment to add to the base URL
        :param data_format: The format of data to be exported, example rdf/json
        :return: <response>
        """
        cert = self.cert
        headers = self.headers
        query = constants.EXPORT_QUERY
        variables = {'data_format': data_format}
        response = None
        try:
            response = self.req_handler.post(appender=appender, headers=headers, query=query,
                                             variables=variables, cert=cert)
        except Exception as err:
            raise Exception(f"Something went wrong with the export request... {json.dumps(response.json())}") from err
        assert_equal(response.json()['data']['export']['response']['code'], 'Success')
        assert_equal(response.json()['data']['export']['response']['message'], 'Export completed.')
        logger.info('Export successfully completed')
