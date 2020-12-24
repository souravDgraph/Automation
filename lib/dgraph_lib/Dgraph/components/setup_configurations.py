import json
import pathlib
from robot.api import logger


class DgraphCLI:

    def __init__(self):
        self.cfg = {}
        self.acl = False
        self.enc = False
        self.tls = False
        self.tls_mutual = False
        self.curr_path = str(pathlib.PurePath(pathlib.Path().absolute()))
        curr_dir = str(pathlib.Path.cwd())
        self.curr_path = curr_dir + "/"
        # curr_dir = curr_dir.split("Automation/", 1)[1]
        # self.curr_path = self.curr_path.split(curr_dir, 1)[0]
        DgraphCLI.read_config(self)

    def get_acl(self):
        return self.acl

    def get_enc(self):
        return self.enc

    def get_tls(self):
        return self.tls

    def get_tls_mutual(self):
        return self.tls_mutual

    def read_config(self):
        """
        Method to set the configurations based on conf/dgraph/conf_dgraph.json
        :return:
        """
        conf_path = self.curr_path + "conf/dgraph/conf_dgraph.json"
        logger.info("configuration path: " + conf_path)
        with open(conf_path) as f:
            self.cfg = json.load(f)
        if self.cfg['acl']['is_enabled']:
            self.acl = True
        if self.cfg['enc']['is_enabled']:
            self.enc = True
        if self.cfg['tls']['is_enabled']:
            self.tls = True
        if self.cfg['tls']['mutual_tls']['is_enabled']:
            self.tls_mutual = True

    def build_zero_alpha_cli(self, cli_name):

        cli_name = cli_name.lower()
        cli_command = "dgraph " + cli_name + " "
        appender = ""
        cli_command = cli_command + "--cache_mb=6000 --badger.compression=zstd:3 --logtostderr -v=2 " \
                                    "--whitelist=0.0.0.0 " \
                                    "--zero=localhost:5080" if cli_name.lower() == "alpha" else cli_command

        if self.acl and cli_name == "alpha":
            acl_path = self.curr_path + self.cfg['acl']['location']
            appender = appender + " --acl_secret_file=" + acl_path
        if self.enc and cli_name == "alpha":
            enc_path = self.curr_path + self.cfg['enc']['location']
            appender = appender + " --encryption_key_file " + enc_path
        if self.tls_mutual:
            for key in self.cfg['tls']['mutual_tls']:
                if self.cfg['tls']['mutual_tls'][key] and key != "is_enabled":
                    appender = appender + " --tls_client_auth " + key
            tsl_location = self.curr_path + self.cfg['tls']['location']
            tls = {
                "--tls_cacert": tsl_location + "/ca.crt",
                "--tls_node_cert": tsl_location + "/node.crt",
                "--tls_node_key": tsl_location + "/node.key",
                "--tls_cert": tsl_location + "/client.groot.crt",
                "--tls_key": tsl_location + "/client.groot.key"
            }
            tls_str = ""
            for key in tls.keys():
                tls_str = tls_str + " " + key + " " + str(tls[key])
            appender = appender + tls_str + " --tls_internal_port_enabled=true "
        elif self.tls:
            tsl_location = self.curr_path + self.cfg['tls']['location']
            tls = {
                "--tls_cacert": tsl_location + "/ca.crt",
                "--tls_node_cert": tsl_location + "/node.crt",
                "--tls_node_key": tsl_location + "/node.key",
            }
            tls_str = ""
            for key in tls.keys():
                tls_str = tls_str + " " + key + " " + str(tls[key])
            appender = appender + tls_str

        cli_command = cli_command + appender + " 2>&1"
        return cli_command

    def build_live_loader_command(self, rdf_file, schema_file):
        """
        Method to build live loader cli command
        :return: live loader cli command
        """
        cli_command = "dgraph live -s " + schema_file + " -f " + rdf_file + " -a localhost:9080 -z localhost:5080 "
        if self.acl:
            cli_command = cli_command + "-u groot -p password"

        tls_str = ""
        if self.tls_mutual:
            tsl_location = self.curr_path + self.cfg['tls']['location']
            tls = {
                "--tls_cacert": tsl_location + "/ca.crt",
                "--tls_cert": tsl_location + "/client.groot.crt",
                "--tls_key": tsl_location + "/client.groot.key"
            }
            for key in tls.keys():
                tls_str = tls_str + " " + key + " " + str(tls[key])
            cli_command = cli_command + tls_str + " --tls_server_name \"localhost\"" + " --tls_internal_port_enabled"

        elif self.tls:
            tsl_location = self.curr_path + self.cfg['tls']['location']
            cli_command = cli_command + " --tls_server_name \"localhost\"" + "--tls_cacert " + tsl_location + "/ca.crt"

        return cli_command
