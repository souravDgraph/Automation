"""
Setup Library
"""
__all__ = ["SetupDgraphKeywords"]
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
        To set the configurations head to-> conf/dgraph/conf_dgraph.json
        :param cli_name: <zero | alpha>
        :return: cli_command <returns zero | alpha command>

        Example:
        | Get dgraph cli command | zero

        """

        self.dgraph_cli = DgraphCLI()
        cli_command = self.dgraph_cli.build_zero_cli(**kwargs)
        return cli_command

    def generate_dgraph_alpha_cli_command(self, bulk_path=None, learner=None, zero_address=None,
                                          is_latest_check=None, **kwargs):
        """
        Method to build CLI command for zero and alpha.
        To set the configurations head to-> conf/dgraph/conf_dgraph.json
        :param learner:
        :param is_latest_check:
        :param zero_address:
        :param bulk_path:
        kwargs:
            :param ludicrous_mode: enabled|disabled
        :return: cli_command <returns zero | alpha command>

        Example:
        | Get dgraph cli command | alpha
        | Get dgraph cli command | alpha | ludicrous_mode=enabled

        """
        cli_command = self.dgraph_cli.build_alpha_cli(bulk_path, learner=learner, zero_address=zero_address,
                                                      is_latest_check=is_latest_check, **kwargs)
        return cli_command

    def get_zero_and_alpha_docker_cli_command(
            self,
            container_name,
            dgraph_version,
            zero_count=1,
            alpha_count=1,
            bulk_path=None,
    ):
        """
        Method to generate zero docker cli command
        :param bulk_path: Bulk Path for alpha directory
        :param alpha_count: alpha count for docker
        :param zero_count: zero count for docker
        :param container_name:  container name for docker
        :param dgraph_version: version of dgraph for docker image
        :return: <list of services for alpha and zero>
        """
        self.dgraph_cli = DgraphCLI(is_docker=True)
        alpha_zero_docker_cli_command_list = (
            self.dgraph_cli.build_docker_zero_and_alpha_cli_command(
                zero_count=zero_count,
                alpha_count=alpha_count,
                bulk_path=bulk_path,
                container_name=container_name,
                dgraph_version=dgraph_version,
            )
        )
        return alpha_zero_docker_cli_command_list

    def get_dgraph_loader_command(
            self,
            rdf_file,
            schema_file,
            loader_type,
            is_latest_version=None,
            docker_string=None,
            is_learner=None,
            zero_host_name=None,
            alpha_host_name=None,
            zero_address=None,
            alpha_address=None,
            out_dir=None,
    ):
        """
        Method to build CLI command for live | bulk loading
        To set the configurations head to-> conf/dgraph/conf_dgraph.json
        :param out_dir:
        :param alpha_address:
        :param zero_address:
        :param alpha_host_name:
        :param is_learner:
        :param zero_host_name:
        :param rdf_file: <path to rdf file>
        :param schema_file: <path to schema file>
        :param loader_type: <live | bulk>
        :param is_latest_version:
        :param docker_string: <if executing on docker>
        :param offset: <offset value set for alpha and zero>
        :return: loader_command <returns live loader command>

        Example:
        | Get Dgraph Loader Command | <rdf_file_path> | <schema_file_path>

        """
        loader_command = self.dgraph_cli.build_loader_command(
            rdf_file=rdf_file,
            schema_file=schema_file,
            loader_type=loader_type,
            latest_version_check=is_latest_version,
            docker_string=docker_string,
            zero_host_name=zero_host_name,
            alpha_host_name=alpha_host_name,
            zero_address=zero_address,
            alpha_address=alpha_address,
            out_dir=out_dir,
            is_learner=is_learner
        )
        return loader_command

    def get_dgraph_increment_command(
            self,
            is_latest_version=None,
            docker_string=None,
            alpha_host_name=None,
            alpha_address=None,
    ):
        """
        Method to generate increment command for dgraph.
        :param alpha_address:
        :param alpha_host_name:
        :param alpha_offset: <offset value set for alpha> | default : 0
        :param is_latest_version:
        :param docker_string:

        Example:
        | Get Dgraph Increment Command | <alpha_offset> |
        | Get Dgraph Increment Command |
        | Get Dgraph Increment Command | 100 |

        """
        inc_command = self.dgraph_cli.build_increment_cli_command(
            is_latest_version,
            docker_string,
            alpha_host_name=alpha_host_name,
            alpha_address=alpha_address,
        )
        return inc_command

    def get_acl_value(self, is_docker=False):
        """
        Method to get ACL prop from config file.
        \n:return: true | false

        Example:
        | Get acl value |
        """
        self.dgraph_cli = DgraphCLI(is_docker=is_docker)
        return self.dgraph_cli.get_acl()

    def get_tls_value(self, is_docker=False):
        """
        Method to get TLS prop from config file.
        \n:return: true | false

        Example:
        | Get tls value |
        """
        self.dgraph_cli = DgraphCLI(is_docker)
        return self.dgraph_cli.get_tls()

    def get_enc_value(self, is_docker=False):
        """
        Method to get ENC prop from config file.
        \n:return: true | false

        Example:
        | Get enc value |
        """
        self.dgraph_cli = DgraphCLI(is_docker)
        return self.dgraph_cli.get_enc()

    def get_tls_certificates(self, is_docker=False):
        """
        Method to get tls and mtls certificates depending on config file.
        :return: <list of certs for tls and mtls>
        """
        self.dgraph_cli = DgraphCLI(is_docker)
        return self.dgraph_cli.get_tls_certs()

    def get_enc_file(self, is_docker=False):
        """
        Method to get the encryption file.
        :return:<encryption file>
        """
        self.dgraph_cli = DgraphCLI(is_docker=is_docker)
        self.dgraph_cli.get_enc()

    @staticmethod
    def check_dgraph_version(version):
        """
        Method to check the dgraph version
        :param version:
        :return:
        """
        return DgraphCLI.check_version(version)

    def set_dgraph_version(self, version=None, branch=None):
        """
        Method to get dgraph local version
        :param version:
        :param branch:
        :return:
        """
        return self.dgraph_cli.set_dgraph_version(version=version, branch=branch)

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
        self.dgraph_cli = DgraphCLI(is_docker=True)
        return self.dgraph_cli.set_dgraph_version(version, branch)
