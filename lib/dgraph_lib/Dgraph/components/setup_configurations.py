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
        self.curr_path = str(pathlib.PurePath(pathlib.Path().absolute()))
        curr_dir = str(pathlib.Path.cwd())
        self.curr_path = curr_dir + "/"
        DgraphCLI.read_config(self)

    def get_acl(self):
        """
        Method to get the ACL flag value
        :return: acl_flag
        """
        return self.acl

    def get_enc(self):
        """
        Mehtod to get the ENC flag value
        :return: enc_flag
        """
        return self.enc

    def get_tls(self):
        """
        Method to get TLS flag value
        :return: tls_flag
        """
        return self.tls

    def get_tls_mutual(self):
        """
        Method to get mTLS flag value.
        :return: mTLS_flag
        """
        return self.tls_mutual

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

    def build_zero_alpha_cli(self, cli_name):
        """
        Method to generate zero and alpha commands based on conf.
        :param cli_name:
        :return:
        """

        cli_name = cli_name.lower()
        cli_command = "dgraph " + cli_name + " "
        appender = ""
        cli_command = cli_command + "--cache_mb=6000 --badger.compression=zstd:3" \
                                    " --logtostderr -v=2 --whitelist=0.0.0.0 " \
                                    "--zero=localhost:5080" \
            if cli_name.lower() == "alpha" else cli_command

        if cli_name == "alpha":
            if self.acl:
                acl_path = self.curr_path + self.cfg['acl']['location']
                appender = appender + " --acl_secret_file=" + acl_path
            if self.enc:
                enc_path = self.curr_path + self.cfg['enc']['location']
                appender = appender + " --encryption_key_file " + enc_path
        if self.tls_mutual:
            for key in self.cfg['tls']['mutual_tls']:
                if self.cfg['tls']['mutual_tls'][key] and key != "is_enabled":
                    appender = appender + " --tls_client_auth " + key
            tls_location = self.curr_path + self.cfg['tls']['location']
            tls = {
                "--tls_cacert": tls_location + "/ca.crt",
                "--tls_node_cert": tls_location + "/node.crt",
                "--tls_node_key": tls_location + "/node.key",
                "--tls_cert": tls_location + "/client.groot.crt",
                "--tls_key": tls_location + "/client.groot.key"
            }
            tls_str = ""
            for key in tls:
                tls_str = tls_str + " " + key + " " + str(tls[key])
            appender = appender + tls_str + " --tls_internal_port_enabled=true "
        elif self.tls:
            tls_location = self.curr_path + self.cfg['tls']['location']
            tls = {
                "--tls_cacert": tls_location + "/ca.crt",
                "--tls_node_cert": tls_location + "/node.crt",
                "--tls_node_key": tls_location + "/node.key",
            }
            tls_str = ""
            for key in tls:
                tls_str = tls_str + " " + key + " " + str(tls[key])
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
        if self.acl and loader_type != "bulk":
            cli_command = cli_command + "-u groot -p password"

        tls_str = ""
        if self.tls_mutual:
            tls_location = self.curr_path + self.cfg['tls']['location']
            tls = {
                "--tls_cacert": tls_location + "/ca.crt",
                "--tls_cert": tls_location + "/client.groot.crt",
                "--tls_key": tls_location + "/client.groot.key"
            }
            for key in tls:
                tls_str = tls_str + " " + key + " " + str(tls[key])
            cli_command = cli_command + tls_str + " --tls_server_name \"localhost\"" + \
                          " --tls_internal_port_enabled"

        elif self.tls:
            tls_location = self.curr_path + self.cfg['tls']['location']
            cli_command = cli_command + " --tls_server_name \"localhost\"" + \
                          "--tls_cacert " + tls_location + "/ca.crt"

        return cli_command
