"""
Setup Library
"""
__all__ = ['SetupDgraphKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "krishna@dgraph.io"
__status__ = "Staging"

from Dgraph.components.setup_configurations import DgraphCLI
# pylint: disable=C0301


class SetupDgraphKeywords:
    """
    Setup Library Keywords
    """

    def __init__(self):
        self.dgraph_cli = DgraphCLI

    def generate_dgraph_zero_cli_command(self):
        """
        Method to build CLI command for zero and alpha.
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param cli_name: <zero | alpha>
        \n:return: cli_command <returns zero | alpha command>

        Example:
        | Get dgraph cli command | zero
        | Get dgraph cli command | alpha

        """

        self.dgraph_cli = DgraphCLI()
        cli_command = self.dgraph_cli.build_zero_cli()
        return cli_command

    def generate_dgraph_alpha_cli_command(self, bulk_path=None):
        """
        Method to build CLI command for zero and alpha.
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param cli_name: <zero | alpha>
        \n:return: cli_command <returns zero | alpha command>

        Example:
        | Get dgraph cli command | zero
        | Get dgraph cli command | alpha

        """

        self.dgraph_cli = DgraphCLI()
        cli_command = self.dgraph_cli.build_alpha_cli(bulk_path)
        return cli_command

    def get_dgraph_loader_command(self, rdf_file, schema_file, loader_type):
        """
        Method to build CLI command for live | bulk loading
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param rdf_file: <path to rdf file>
        \n:param schema_file: <path to schema file>
        \n:param loader_type: <live | bulk>
        \n:return: loader_command <returns live loader command>

        Example:
        | Get Dgraph Loader Command | <rdf_file_path> | <schema_file_path>

        """

        self.dgraph_cli = DgraphCLI()
        loader_command = self.dgraph_cli.build_loader_command(rdf_file, schema_file, loader_type)
        return loader_command

    def get_acl_value(self):
        """
        Method to get ACL prop from config file.
        \n:return: true | false

        Example:
        | Get acl value |
        """
        self.dgraph_cli = DgraphCLI()
        return self.dgraph_cli.get_acl()

    def get_tls_value(self):
        """
        Method to get TLS prop from config file.
        \n:return: true | false

        Example:
        | Get tls value |
        """
        self.dgraph_cli = DgraphCLI()
        return self.dgraph_cli.get_tls()

    def get_enc_value(self):
        """
        Method to get ENC prop from config file.
        \n:return: true | false

        Example:
        | Get enc value |
        """
        self.dgraph_cli = DgraphCLI()
        return self.dgraph_cli.get_enc()

    def get_tls_certificates(self):
        """
        Method to get tls and mtls certificates depending on config file.
        :return: <list of certs for tls and mtls>
        """
        self.dgraph_cli = DgraphCLI()
        return self.dgraph_cli.get_tls_certs()

    def get_enc_file(self):
        """
        Method to get the encryption file.
        :return:<encryption file>
        """
        self.dgraph_cli.get_enc()

    @staticmethod
    def check_dgraph_version(version):
        """
        Method to check the dgraph version
        :param version:
        :return:
        """
        DgraphCLI.check_version(version)

    def get_dgraph_details(self, dgraph_details_key):
        """
        Method to get the dgraph version details.
        :param dgraph_details_key:
        :return:<value>
        """
        return self.dgraph_cli.get_dgraph_version_details(dgraph_details_key)
