"""
PyDgraph Library
"""
__all__ = ['PydgraphKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"

# pylint: disable=W0201, C0301
from robot.api import logger
from Common.components.pydgraph_configuration import PydgraphOperations


class PydgraphKeywords:
    """
    PyDgraph Library Keywords
    """

    def pyd_create_insecure_connection(self, address):
        """
        Method to create a Pydgraph client connection for gRPC request.
        \n
        \n:param address: <address>
        \n:return: <return the connection>

        Example:
        | Pyd create connection | aplha_gRPC_url |
        | Pyd create connection | localhost:9080
        """
        return self.py_client.client_connection(address)

    def pyd_create_mtls_connection(self, address, loc=None, username=None):
        """
        Method to create mTLS client connection for specified user.
        \n optional parameters are loc, username and password
        \n:param address: <connection_address>
        \n:param loc: <path to tls folder>
        \n:param username: <client_username>
        \n:param password: <client_password>
        \n:return: <client_obj>

         Example:
        | Pyd create mtls custom connection | aplha_gRPC_url | loc | username | password
        | Pyd create mtls custom connection | localhost:9080 | <path> | groot | password
        | Pyd create mtls custom connection | localhost:9080
        """
        self.py_client = PydgraphOperations()
        res_client = ""
        if loc:
            res_client = self.py_client.custom_client_connect(address, mtls=True, loc=loc)
        elif username:
            res_client = self.py_client.custom_client_connect(address, mtls=True, username=username)
        elif loc and username:
            res_client = self.py_client.custom_client_connect(address, mtls=True, loc=loc, username=username)
        else:
            res_client = self.py_client.custom_client_connect(address, mtls=True)
        return res_client

    def pyd_create_acl_connection(self, address, username=None, password=None):
        """
        Method to create mTLS client connection for specified user.
        \n optional parameters are loc, username and password
        \n:param address: <connection_address>
        \n:param loc: <path to tls folder>
        \n:param username: <client_username>
        \n:param password: <client_password>
        \n:return: <client_obj>

         Example:
        | Pyd create mtls custom connection | aplha_gRPC_url | loc | username | password
        | Pyd create mtls custom connection | localhost:9080 | <path> | groot | password
        | Pyd create mtls custom connection | localhost:9080
        """
        self.py_client = PydgraphOperations()
        res_client = ""
        if username and password:
            res_client = self.py_client.custom_client_connect(address, acl=True,
                                                              username=username, password=password)
        else:
            res_client = self.py_client.custom_client_connect(address, acl=True)
        return res_client

    def pyd_create_acl_and_mtls_connection(self, address, loc=None, username=None, password=None):
        """
        Method to create mTLS client connection for specified user.
        \n optional parameters are loc, username and password
        \n:param address: <connection_address>
        \n:param loc: <path to tls folder>
        \n:param username: <client_username>
        \n:param password: <client_password>
        \n:return: <client_obj>

         Example:
        | Pyd create mtls custom connection | aplha_gRPC_url | loc | username | password
        | Pyd create mtls custom connection | localhost:9080 | <path> | groot | password
        | Pyd create mtls custom connection | localhost:9080
        """
        self.py_client = PydgraphOperations()
        res_client = ""
        if loc and username and password:
            logger.info("Creating mTLS connection with custom parameters.")
            res_client = self.py_client.custom_client_connect(address, acl=True, mtls=True,
                                                              loc=loc, username=username, password=password)
        else:
            logger.info("Creating mTLS connection with default parameters.")
            res_client = self.py_client.custom_client_connect(address, acl=True, mtls=True)
        return res_client

    def pyd_set_schema(self, schema_file_name):
        """
        Method to set schema for the client connection created.
        \n:param schema_file_name: <schema_file_name>
        \n:return: <client_obj>

        Example:
        | Pyd set schema | user_schema
        """
        return self.py_client.set_schema(schema_file_name)

    def pyd_get_data(self, query):
        """
        Method to get the data from the query passed.
        \n:param query: <query>
        \n:return: <query_res>

        Example:
        | Pyd get data | query
        """
        return self.py_client.execute_query(query)

    def pyd_add_json_data(self, json_data):
        """
        Method to create new data using json.
        \n:param json_data: <json_data>
        \n:return: <response>

        Example:
        | Pyd add json data | json_data
        """
        return self.py_client.create_new_data(json_data)

    def pyd_drop_all_data(self):
        """
        Method to drop all the data in the db
        \n:return:<null>
        """
        self.py_client.client_drop_all()
