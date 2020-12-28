"""
Setup Library
"""
__all__ = ['SetupDgraphKeywords']
__author__ = "Krishna Kaushik"
__version__ = "1.0"
__maintainer__ = "Krishna Kaushik"
__email__ = "tkrishnakaushik96@gmail.com"
__status__ = "Stagging"

from Dgraph.components.setup_configurations import DgraphCLI


class SetupDgraphKeywords:
    """
    Setup Library Keywords
    """

    def __init__(self):
        self.dgraph_cli = DgraphCLI

    def get_dgraph_cli_command(self, cli_name):
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
        cli_command = self.dgraph_cli.build_zero_alpha_cli(cli_name)
        return cli_command

    def get_dgraph_loader_command(self, rdf_file, schema_file, loader_type):
        """
        Method to build CLI command for live | bulk loading
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param rdf_file: <path to rdf file>
        \n:param schema_file: <path to schema file>
        \n:param loader_type: <live | bulk>
        \n:return: live_loader_command <returns live loader command>

        Example:
        | Get dgraph live loader command | <rdf_file_path> | <schema_file_path>

        """

        self.dgraph_cli = DgraphCLI()
        live_loader_command = self.dgraph_cli.build_loader_command(rdf_file, schema_file, loader_type)
        return live_loader_command

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
