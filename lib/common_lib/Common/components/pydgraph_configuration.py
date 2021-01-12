"""
PyDgraph configurations class
"""
import json
import grpc
import pydgraph
from pydgraph import Txn
from robot.api import logger
from Dgraph.components.setup_configurations import DgraphCLI

# pylint: disable=C0301, E1121, R0914, W0201, W0703, R0913

__all__ = ['PydgraphOperations']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"


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
        logger.info("Establishing Client connection at:  " + address)
        self.client_stub = pydgraph.DgraphClientStub(address)
        self.client = pydgraph.DgraphClient(self.client_stub)
        logger.info("Dgraph client connection is established using gRPC.")
        return self.client

    def custom_client_connect(self, address, acl=False, mtls=False, loc=None, username=None, password=None):
        """
        Mehtod to create gRPC client connection for mtls and acl.
        :param address:
        :param acl:
        :param mtls:
        :param loc:
        :param username:
        :param password:
        :return:
        """
        logger.info("Creating client...")
        if mtls:
            if loc and username:
                creds = PydgraphOperations.create_mtls_connect(self, address, loc, username)
            else:
                creds = PydgraphOperations.create_mtls_connect(self, address)

        client_stub = pydgraph.DgraphClientStub(address, credentials=creds)
        self.client = pydgraph.DgraphClient(client_stub)
        logger.info("client connection created.")
        if acl:
            if username and password:
                PydgraphOperations.create_acl_connection(self, username, password)
            else:
                PydgraphOperations.create_acl_connection(self)
        return self.client

    def create_mtls_connect(self, address, cust_loc=None, cust_username=None):
        """
        Method to perform mTLS connection using gRPC port.
        :param address: gRPC alpha port address
        :param cust_loc: client certificates location
        :param cust_username: client username
        :return:
        """

        logger.info("Establishing mTLS client connection at: " + address)
        dgraph_cli = DgraphCLI()
        loc = dgraph_cli.get_tls_location()
        username = "groot"

        if cust_loc:
            loc = cust_loc
        if cust_username:
            username = cust_username
        logger.info(loc)
        try:
            # Read certs
            logger.debug("Reading ca certificate..")
            with open(loc + "/ca.crt", 'rb') as ca_f:
                root_ca_cert = ca_f.read()
            logger.debug("ca certificate is read.")

            logger.debug("Reading client certificates..")
            client_cert_key = None
            client_cert = None
            if dgraph_cli.get_mtls_verification_type() == "REQUIREANDVERIFY":
                with open(loc + "/client." + username + ".key", 'rb') as client_key_f:
                    client_cert_key = client_key_f.read()
                with open(loc + "/client." + username + ".crt", 'rb') as client_cert_f:
                    client_cert = client_cert_f.read()
            logger.debug("Client Certificates are read.")

        except FileNotFoundError as file_not_fount_err:
            logger.debug("debug loading the file " + file_not_fount_err)

        try:
            # Connect to Dgraph via gRPC with mutual TLS.
            if client_cert and client_cert_key:
                creds = grpc.ssl_channel_credentials(root_certificates=root_ca_cert,
                                                     private_key=client_cert_key,
                                                     certificate_chain=client_cert)
            else:
                creds = grpc.ssl_channel_credentials(root_certificates=root_ca_cert)

            logger.info("Dgraph mTLS client connection established using gRPC....")
        except Exception as error:
            # Need to check what all different debugs we get and update the Exception accordingly
            logger.debug("Exception occurred while creating mtls connection:  ", loc, error)
        return creds

    def create_acl_connection(self, cust_username=None, cust_password=None):
        """
        Method to perform login as part of ACL connection
        :param username:
        :param password:
        :return:
        """
        username = "groot"
        password = "password"

        if cust_username and cust_username:
            username = cust_username
            password = cust_password

        logger.info("ACL check-> Logging in with username:" + username)

        try:
            self.client.login(username, password)
            logger.info("Dgraph ACL login successful....")
        except Exception as error:
            # Need to check what all different debugs we get and update the Exception accordingly
            logger.debug("Exception occurred while logging in with user and pass:  ", username, password, error)
        return self.client

    # Drop All - discard all data and start from a clean slate.
    def client_drop_all(self):
        """
        Method to drop all the data in db.
        \n:return: <client connection>
        """
        logger.info("dropping all the data in db")
        return self.client.alter(pydgraph.Operation(drop_all=True))

    def set_schema(self, schema_file):
        """
        Method to set schema to the client connection.
        :param schema_file: <schema_file_name>
        :return: <schema_updated_client>
        """
        dgraph_cli = DgraphCLI()
        with open(dgraph_cli.get_test_data_location() + schema_file, 'r') as schema_context:
            schema_structure = schema_context.read()
        logger.info("Setting Schema to the client connection created.")
        schema_op = pydgraph.Operation(schema=schema_structure)
        self.client.alter(schema_op)
        return self.client

    def execute_query(self, query):
        """
        Method to execute the query and return the response.
        \n:param query:
        \n:return:
        """
        logger.info("Executing the query")
        response = self.client.txn(read_only=True).query(query=query)
        logger.info(response)
        return response

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
            response = self.client.txn(read_only=True).query(query, variables=variables)
            peoplelist = json.loads(response.json)
            for person in peoplelist['all']:
                txn.mutate(del_obj=person)
            txn.commit()

        finally:
            txn.discard()
