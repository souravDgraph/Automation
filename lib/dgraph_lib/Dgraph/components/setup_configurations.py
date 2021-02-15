"""
Python class to generated Dgraph commands based on configurations.
"""
import json
import pathlib
from robot.api import logger


class DgraphCLI:
    """
    Class to generate the cli-commands based on configurations.
    """

    def __init__(self):
        self.cfg = {}
        self.acl = False
        self.enc = False
        self.tls = False
        self.tls_mutual = False
        self.tls_mutual_flags = []
        self.curr_path = str(pathlib.PurePath(pathlib.Path().absolute()))
        curr_dir = str(pathlib.Path.cwd())
        self.curr_path = curr_dir + "/"
        DgraphCLI.read_config(self)
        logger.info("Dgraph Configurations are ready to load.")

    def get_test_data_location(self):
        """
        Method to get test-data location for Dgraph
        :return:
        """
        return self.curr_path + "test_data/datasets/"

    def get_acl(self):
        """
        Method to get the ACL flag value
        :return: acl_flag
        """
        logger.debug(self.acl)
        return self.acl

    def get_enc(self):
        """
        Mehtod to get the ENC flag value
        :return: enc_flag
        """
        logger.debug(self.enc)
        return self.enc

    def get_tls(self):
        """
        Method to get TLS flag value
        :return: tls_flag
        """
        logger.debug(self.tls)
        return self.tls

    def get_tls_mutual(self):
        """
        Method to get mTLS flag value.
        :return: mTLS_flag
        """
        logger.debug(self.tls_mutual)
        return self.tls_mutual

    def get_tls_location(self):
        """
        Method to get the tls location
        :return: <path_tls_location>
        """
        tls_loc = self.cfg['tls']['location']
        logger.debug(self.curr_path + tls_loc)
        return self.curr_path + tls_loc

    def get_tls_certs(self, cli):
        """
        Method to get all the certificates for tls or mtls configuration
        :return:<mtls_certificates>
        """
        logger.debug("Appending TLS and mTLS certificates.")
        tls_location = self.curr_path + self.cfg['tls']['location']
        tls_cert = ""
        if self.tls_mutual:
            mtls = {
                "--tls_cacert": tls_location + "/ca.crt",
                "--tls_cert": tls_location + "/client.groot.crt",
                "--tls_key": tls_location + "/client.groot.key"
            }
        elif self.tls:
            mtls = {
                "--tls_cacert": tls_location + "/ca.crt",
            }
        if self.tls or self.tls_mutual:
            if cli == "zero" or cli == "alpha":
                mtls.update({
                    "--tls_node_cert": tls_location + "/node.crt",
                    "--tls_node_key": tls_location + "/node.key"
                })
            for key in mtls:
                tls_cert = tls_cert + " " + key + " " + str(mtls[key])
        logger.debug(tls_cert)
        return tls_cert

    def get_mtls_verification_type(self):
        """
        Method to get the verification type specified in conf file.
        :return:
        """
        verification_type = None
        for key in self.cfg['tls']['mutual_tls']:
            if self.cfg['tls']['mutual_tls'][key] and key != "is_enabled":
                verification_type = key
        return verification_type

    def read_config(self):
        """
        Method to set the configurations based on conf/dgraph/conf_dgraph.json
        :return:
        """
        conf_path = self.curr_path + "conf/dgraph/conf_dgraph.json"
        logger.info("configuration path: " + conf_path)
        with open(conf_path) as conf_file:
            self.cfg = json.load(conf_file)
        if self.cfg['acl']['is_enabled']:
            self.acl = True
        if self.cfg['enc']['is_enabled']:
            self.enc = True
        if self.cfg['tls']['is_enabled']:
            self.tls = True
        if self.cfg['tls']['mutual_tls']['is_enabled']:
            self.tls_mutual = True

    def build_zero_cli(self):
        """
        Method to generate zero commands based on conf.
        :return:
        """

        cli_name = "zero"
        cli_command = "dgraph " + cli_name + " "
        appender = ""

        # Configure tls and mtls
        tls_str = self.get_tls_certs("zero")
        if self.tls_mutual:
            for key in self.cfg['tls']['mutual_tls']:
                if self.cfg['tls']['mutual_tls'][key] and key != "is_enabled":
                    appender = appender + " --tls_client_auth " + key
            appender = appender + tls_str + " --tls_internal_port_enabled=true "
        elif self.tls:
            appender = appender + tls_str

        cli_command = cli_command + appender + " 2>&1"
        return cli_command

    def build_alpha_cli(self, bulk_path=None):
        """
        Method to generate alpha commands based on conf.
        \n accepts one param for bulk data initializing
        :param bulk_path: <bulk loader data path>
        :return:
        """

        cli_name = "alpha"
        cli_command = "dgraph " + cli_name + " "
        appender = ""
        cli_command = cli_command + "--cache_mb=6000" \
                                    " -v=2 --whitelist=0.0.0.0 " \
                                    "--zero=localhost:5080"
        if bulk_path:
            appender = appender + " -p " + bulk_path
        if self.acl:
            acl_path = self.curr_path + self.cfg['acl']['location']
            appender = appender + " --acl_secret_file=" + acl_path
        if self.enc:
            enc_path = self.curr_path + self.cfg['enc']['location']
            appender = appender + " --encryption_key_file " + enc_path

        # Configure tls and mtls
        tls_str = self.get_tls_certs("alpha")
        if self.tls_mutual:
            for key in self.cfg['tls']['mutual_tls']:
                if self.cfg['tls']['mutual_tls'][key] and key != "is_enabled":
                    appender = appender + " --tls_client_auth " + key
            appender = appender + tls_str + " --tls_internal_port_enabled=true "
        elif self.tls:
            appender = appender + tls_str

        cli_command = cli_command + appender + " 2>&1"
        return cli_command

    def build_loader_command(self, rdf_file, schema_file, loader_type):
        """
        Method to build bulk/live loader cli command
        :return: live loader cli command
        """

        loader_type = loader_type.lower()

        cli_command = ""
        if loader_type == "live":
            cli_command = "dgraph " + loader_type + " -s " + schema_file + \
                          " -f " + rdf_file + " -a localhost:9080 -z localhost:5080 "
        elif loader_type == "bulk":
            cli_command = "dgraph " + loader_type + " -s " + schema_file + " -f " + \
                          rdf_file + " --map_shards=2 --reduce_shards=1 --http " \
                                     "localhost:8000 --zero=localhost:5080 "
            if self.enc:
                enc_path = self.curr_path + self.cfg['enc']['location']
                cli_command = cli_command + " --encrypted=False  --encrypted_out=True " \
                                            "--encryption_key_file " + enc_path
        if self.acl and loader_type != "bulk":
            cli_command = cli_command + " --creds 'user=groot;password=password' "
        #     cli_command = cli_command + " -u groot -p password"

        mtls_certs = self.get_tls_certs("live")
        if self.tls_mutual:
            cli_command = cli_command + mtls_certs + " --tls_server_name \"localhost\"" + \
                          " --tls_internal_port_enabled"
        elif self.tls:
            cli_command = cli_command + mtls_certs + " --tls_server_name \"localhost\""
        return cli_command
