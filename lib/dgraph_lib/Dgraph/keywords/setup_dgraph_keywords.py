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

    def generate_dgraph_zero_cli_command(self, **kwargs):
        """
        Method to build CLI command for zero and alpha.
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param cli_name: <zero | alpha>
        \n:return: cli_command <returns zero | alpha command>

        Example:
        | Get dgraph cli command | zero

        """

        self.dgraph_cli = DgraphCLI()
        cli_command = self.dgraph_cli.build_zero_cli(**kwargs)
        return cli_command

    def generate_dgraph_alpha_cli_command(self, bulk_path=None, **kwargs):
        """
        Method to build CLI command for zero and alpha.
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param cli_name: <zero | alpha>
        \nkwargs:
            \n:param ludicrous_mode: enabled|disabled
        \n:return: cli_command <returns zero | alpha command>

        Example:
        | Get dgraph cli command | alpha
        | Get dgraph cli command | alpha | ludicrous_mode=enabled

        """
        cli_command = self.dgraph_cli.build_alpha_cli(bulk_path, **kwargs)
        return cli_command

    def get_dgraph_loader_command(self, rdf_file, schema_file, loader_type, is_latest_version: None,
                                  docker_string=None, offset=0):
        """
        Method to build CLI command for live | bulk loading
        \nTo set the configurations head to-> conf/dgraph/conf_dgraph.json
        \n:param rdf_file: <path to rdf file>
        \n:param schema_file: <path to schema file>
        \n:param loader_type: <live | bulk>
        \n:param is_latest_version:
        \n:param docker_string: <if executing on docker>
        \n:param offset: <offset value set for alpha and zero>
        \n:return: loader_command <returns live loader command>

        Example:
        | Get Dgraph Loader Command | <rdf_file_path> | <schema_file_path>

        """
        loader_command = self.dgraph_cli.build_loader_command(rdf_file, schema_file, loader_type, is_latest_version,
                                                              docker_string, offset=offset)
        return loader_command

    def get_dgraph_increment_command(self, is_latest_version: None, docker_string=None, alpha_offset: int = 0):
        """
        Method to generate increment command for dgraph.
        :param alpha_offset: <offset value set for alpha> | default : 0
        :param is_latest_version:
        :param docker_string:

        Example:
        | Get Dgraph Increment Command | <alpha_offset> |
        | Get Dgraph Increment Command |
        | Get Dgraph Increment Command | 100 |

        """
        inc_command = self.dgraph_cli.build_increment_cli_command(is_latest_version, docker_string, alpha_offset)
        return inc_command

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
        self.dgraph_cli = DgraphCLI()
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

    def set_execution_to_docker(self, version, branch):
        """
        Method to set DgaphCLI to docker mode.
        """
        self.dgraph_cli = DgraphCLI()
        return self.dgraph_cli.set_dgraph_version(version, branch)
