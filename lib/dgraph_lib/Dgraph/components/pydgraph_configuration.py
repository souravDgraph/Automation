"""
PyDgraph configurations class
"""
import json
import grpc
import pydgraph

from Dgraph.components.setup_configurations import DgraphCLI
from pydgraph import Txn
from robot.api import logger

# pylint: disable=C0301, E1121, R0914, W0201, W0703


class PydgraphOperations:
    """
    Methods defined using Pydgraph Operations.
    """

    def client_connection(self, address):
        """
        Method to create a dgraph client connection without mTLS using gRPC address.
        :param address:
        :return:
        """
        logger.info("Establishing Client connection")
        self.client_stub = pydgraph.DgraphClientStub(address)
        self.client = pydgraph.DgraphClient(self.client_stub)
        logger.info("Dgraph client connection is established using gRPC.")
        return self.client

    def create_client_connect_with_login(self, address, loc=None, username=None, password=None):
        """
        Method to create mTLS client connection using gRPC address.
        :param address:
        :param loc:
        :param username:
        :param password:
        :return:
        """
        logger.info("Establishing mTLS client connection.")
        dgraph_cli = DgraphCLI()
        def_loc = dgraph_cli.get_tls_location()
        def_username = "groot"
        def_password = "password"

        if loc:
            def_loc = loc
        if username:
            def_username = username
        if password:
            def_password = password

        # Read certs
        with open(def_loc + '/ca.crt', 'rb') as ca_f:
            root_ca_cert = ca_f.read()
        with open(def_loc + '/client.' + def_username + '.key', 'rb') as client_key_f:
            client_cert_key = client_key_f.read()
        with open(def_loc + '/client.' + def_username + '.crt', 'rb') as client_cert_f:
            client_cert = client_cert_f.read()

        try:
            # Connect to Dgraph via gRPC with mutual TLS.
            creds = grpc.ssl_channel_credentials(root_certificates=root_ca_cert,
                                                 private_key=client_cert_key,
                                                 certificate_chain=client_cert)
            client_stub = pydgraph.DgraphClientStub(address, credentials=creds)
            self.client = pydgraph.DgraphClient(client_stub)
            self.client.login(def_username, def_password)
            logger.info("Dgraph mTLS client connection established using gRPC....")
        except Exception as error:
            # Need to check what all different errors we get and update the Exception accordingly
            logger.debug(error)
            logger.debug("Exception occured while creating connection with user and pass:  ", username, password)
        return self.client

    # Drop All - discard all data and start from a clean slate.
    def client_drop_all(self):
        """
        Method to drop all the data in db.
        \n:return: <client connection>
        """
        logger.info("dropping all the data in db")
        return self.client.alter(pydgraph.Operation(drop_all=True))

    def set_schema(self, user_schema):
        """
        Method to set schema to the client connection.
        \n:param user_schema:
        \n:return:
        """
        logger.info("Setting Schema to the client connection created.")
        schema_op = pydgraph.Operation(schema=user_schema)
        self.client.alter(schema_op)
        return self.client

    def execute_query(self, query):
        """
        Method to execute the query and return the response.
        \n:param query:
        \n:return:
        """
        logger.info("Executing the query")
        res = self.client.txn(read_only=True).query(query=query)
        return res

    # Create data using JSON.
    def create_new_data(self, json_data):
        """
        Method to insert new json data to db.
        \n:param json_data:
        \n:return: <response>
        """
        logger.info("Creating new data set to the db.")
        # Create a new transaction.
        txn = self.client.txn()
        response = Txn
        try:
            # Run mutation.
            response = txn.mutate(set_obj=json_data)

            # Commit transaction.
            txn.commit()
            logger.info('Created new data')

        finally:
            # Clean up. Calling this after txn.commit() is a no-op and hence safe.
            txn.discard()
        return response

    # Deleting a data
    def delete_data(self, query, variables):
        """
        Method to delete the data in db. (Still needs workaround.)
        \n:param query:
        \n:param variables:
        \n:return:
        """
        # Create a new transaction.
        txn = self.client.txn()
        try:
            res1 = self.client.txn(read_only=True).query(query, variables=variables)
            ppl1 = json.loads(res1.json)
            for person in ppl1['all']:
                txn.mutate(del_obj=person)
            txn.commit()

        finally:
            txn.discard()
