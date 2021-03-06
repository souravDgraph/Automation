"""
Custom Request Library for Dgraph
"""
__all__ = ["CustomRequestKeywords"]
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


# pylint: disable=R0912, R0915, C0301, W0201


class CustomRequestKeywords:
    """
    Custom Request Keywords Class.
    """

    def connect_request_server(
        self, url=None, port=None, offset=0, is_docker=None, is_learner=None
    ):
        """
        Method to connect to url to perform backup.
        :param is_docker: is execution on docker
        :param offset: offset value for execution
        :param url: url of the excution
        :param port: port of the server
        :return: the instance of RequestHandler object

        Example:
        | connect_request_server | url=None | offset | is_docker
        | connect_request_server | url=https://localhost:8080
        | connect_request_server | url=https://localhost:8080 | 100 | True
        """
        self.headers = constants.COMMON_HEADER
        self.dgraph_cli = DgraphCLI(is_docker=is_docker)
        self.cert = None
        alpha_port = 8080
        if offset != 0:
            self.dgraph_cli.offset = offset
            if is_learner:
                self.dgraph_cli.offset += 1
        else:
            if is_learner:
                offset = self.dgraph_cli.offset + 1
            else:
                offset = self.dgraph_cli.offset
        if url is not None:
            self.req_handler = RequestHandler(url)
        else:
            if port:
                alpha_port = port
            else:
                alpha_port += offset
            if self.dgraph_cli.get_tls():
                url = f"https://localhost:{alpha_port}"
            else:
                url = f"http://localhost:{alpha_port}"
            self.req_handler = RequestHandler(url)

        logger.info("Requested URL: " + url)

        if self.dgraph_cli.get_tls():
            self.cert = self.get_certs()
            logger.info("TLS is configured.")
        if self.dgraph_cli.get_acl():
            self.headers = self.login("/admin")

    def login(self, appender):
        """
        Method to Login to the dgraph server and generate the jwt token
        :param appender: URL segment to append to the base URL

        Example:
        | login | appender
        | login | /admin
        """
        query = constants.LOGIN_BODY
        variables = None
        login_response = self.req_handler.post(
            appender=appender,
            headers=self.headers,
            query=query,
            variables=variables,
            cert=self.cert,
        )
        jwt_token = login_response.json()["data"]["login"]["response"]["accessJWT"]
        return_header = {
            "X-Dgraph-AccessToken": jwt_token,
            "Content-Type": "application/json",
        }
        logger.info("login Successful")
        return return_header

    def get_certs(self):
        """
        Method to get TLS certificates if required by the configuration

        Example:
        | get certs |
        """
        tls_cert = self.dgraph_cli.get_cert_from_pem_file()
        return tls_cert

    def health_status_check(self, appender):
        """
        Method to check the health of the deployed dgraph instance
        :param appender: URL segment to add to the base URL
        :return status: healthy/unhealthy

         Example:
        | health check |  appender
        | health check |  /health
        """
        cert = self.cert
        headers = self.headers
        response = None
        try:
            response = self.req_handler.get(
                appender=appender, headers=headers, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the data params.. {json.dumps(response.json())}"
            ) from err
        status = response.json()[0]["status"]
        return status

    def health_check(self, appender):
        """
        Method to check the health of the deployed dgraph instance
        :param appender: URL segment to add to the base URL
        :return status: healthy/unhealthy

         Example:
        | health check |  appender
        | health check |  /health
        """
        cert = self.cert
        headers = self.headers
        response = None
        try:
            response = self.req_handler.get(
                appender=appender, headers=headers, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the data params.. {json.dumps(response.json())}"
            ) from err
        return response.json()

    def state_check(self, appender):
        """
        Method to check the state of the deployed database instance
        :param appender: URL segment to add to the base URL
        :return state: Complete state of the database

        Example:
        | state check |  appender
        | state check |  /state
        """
        cert = self.cert
        headers = self.headers
        response = None
        try:
            response = self.req_handler.get(
                appender=appender, headers=headers, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the data params.. {json.dumps(response.json())}"
            ) from err
        state = response.json()
        return state

    def state_check(self, appender):
        """
        Method to check the state of the deployed database instance
        :param appender: URL segment to add to the base URL
        :return state: Complete state of the database

        Example:
        | state check |  appender
        | state check |  /state
        """
        cert = self.cert
        headers = self.headers
        response = None
        try:
            response = self.req_handler.get(
                appender=appender, headers=headers, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the data params.. {json.dumps(response.json())}"
            ) from err
        state = response.json()
        return state

    def remove_node(self, appender, alpha_id, group):
        """
        Method to remove alpha node from a cluster, this API sends the request on the zero port and removes a alpha node
        :param appender: URL segment to add to the base URL
        :param alpha_id: ID of the alpha in the cluster (can get this value from state check)
        :param group: group number in which the alpha belongs
        :return: <response>

        Example:
        | remove node |  appender | alpha_id | group
        """
        cert = self.cert
        headers = self.headers
        parameters = {"id": alpha_id, "group": group}
        response = None
        try:
            response = self.req_handler.get(
                appender=appender, headers=headers, parameters=parameters, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the data params.. {json.dumps(response.json())}"
            ) from err
        return response

    def backup_using_admin(self, path):
        """
        Method to call backup GraphQL mutation on dgraph, this will trigger a backup
        :param appender: URL segment to add to the base URL
        :param path: Backup path
        :return: <response>

         Example:
        | backup using admin |  path
        | backup using admin |  /backup/
        """
        cert = self.cert
        headers = self.headers
        query = constants.BACKUP_QUERY
        variables = {"path": path}
        response = None
        appender = "/admin"
        try:
            response = self.req_handler.post(
                appender=appender,
                headers=headers,
                query=query,
                variables=variables,
                cert=cert,
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the backup request.. {json.dumps(response.json())}"
            ) from err
        # assert_equal(response.json()['data']['backup']['response']['code'], 'Success')
        # assert_equal(response.json()['data']['backup']['response']['message'], 'Backup completed.')
        logger.info("Backup successfully initiated")
        return response.json()

    def restore_using_admin(self, path):
        """
        Method to call restore GraphQL mutation on dgraph, this will trigger a restore
        :param appender: URL segment to add to the base URL
        :param path: Path to the restore manifest to trigger a restore
        :return: <response>

        Example:
        | restore using admin |  path
        | restore using admin |  /backup/backup_file_location
        """
        cert = self.cert
        headers = self.headers
        query = constants.RESTORE_QUERY
        if self.dgraph_cli.enc:
            variables = {"path": path, "$enc_file": self.dgraph_cli.get_enc_file()}
        else:
            variables = {"path": path}
        response = None
        appender = "/admin"

        try:
            response = self.req_handler.post(
                appender=appender,
                headers=headers,
                query=query,
                variables=variables,
                cert=cert,
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the restore request.. {json.dumps(response.json())}"
            ) from err
        assert_equal(response.json()["data"]["restore"]["code"], "Success")
        assert_equal(
            response.json()["data"]["restore"]["message"], "Restore operation started."
        )
        logger.info("Restore successfully started")
        return response

    def backup_using_admin_backup(self, path):
        """
        Method to call backup using the /admin/backup API, this does not use a GraphQL request
        :param appender: URL segment to add to the base URL
        :param path: path to backup the database
        :return: <response>

        Example:
        | backup using admin backup |  path
        | backup using admin backup |  /backup/
        """
        cert = self.cert
        headers = self.headers
        payload = {"destination": path}
        response = None
        appender = "/admin/backup"
        try:
            response = self.req_handler.post_request(
                appender=appender, headers=headers, body=payload, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the backup request... {json.dumps(response.json())}"
            ) from err
        # assert_equal(response.json()['data']['backup']['response']['code'], 'Success')
        # assert_equal(response.json()['data']['backup']['response']['message'], 'Backup completed.')
        logger.info("Backup successfully completed")
        return response.json()

    def restore_using_admin_backup(self, path):
        """
        Method to call a restore using the /admin/backup API, this does not use a GraphQL request
        :param appender: URL segment to add to the base URL
        :param path: Path to the restore manifest to the database for triggering restore
        :return: <response>

        Example:
        | restore using admin backup |  path
        | restore using admin backup |  /backup/backup_file_dir/
        """
        cert = self.cert
        headers = self.headers
        payload = {"location": path}
        response = None
        appender = "/admin/backup"
        try:
            response = self.req_handler.post_request(
                appender=appender, headers=headers, body=payload, cert=cert
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the restore request... {json.dumps(response.json())}"
            ) from err
        assert_equal(response.json()["data"]["restore"]["code"], "Success")
        assert_equal(
            response.json()["data"]["restore"]["message"], "Restore operation started."
        )
        logger.info("Restore successfully started")
        return response

    def export_data_admin(self, appender, data_format):
        """
        Method to export the database using the GraphQL export mutation
        :param appender: URL segment to add to the base URL
        :param data_format: The format of data to be exported, example rdf/json
        :return: <response>

        Example:
        | export data admin |  appender | data_format
        """
        cert = self.cert
        headers = self.headers
        query = constants.EXPORT_QUERY
        variables = {"data_format": data_format}
        response = None
        try:
            response = self.req_handler.post(
                appender=appender,
                headers=headers,
                query=query,
                variables=variables,
                cert=cert,
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the export request... {json.dumps(response.json())}"
            ) from err
        assert_equal(response.json()["data"]["export"]["response"]["code"], "Success")
        assert_equal(
            response.json()["data"]["export"]["response"]["message"],
            "Export completed.",
        )
        logger.info("Export successfully completed")
        return response

    def export_nfs_data_admin(self, data_format, destination, appender="/admin"):
        """
        Method to export the database using the GraphQL export mutation
        :param destination: Export data destination
        :param appender: URL segment to add to the base URL
        :param data_format: The format of data to be exported, example rdf/json
        :return: <response>

        Example:
        | export data admin |  appender | data_format
        """
        cert = self.cert
        headers = self.headers
        query = constants.EXPORT_NFS_QUERY
        variables = {"data_format": data_format, "destination": destination}
        response = None
        try:
            response = self.req_handler.post(
                appender=appender,
                headers=headers,
                query=query,
                variables=variables,
                cert=cert,
            )
        except Exception as err:
            raise Exception(
                f"Something went wrong with the export request... {json.dumps(response.json())}"
            ) from err
        assert_equal(response.json()["data"]["export"]["response"]["code"], "Success")
        assert_equal(
            response.json()["data"]["export"]["response"]["message"],
            "Export completed.",
        )
        logger.info("Export successfully completed")
        return response
