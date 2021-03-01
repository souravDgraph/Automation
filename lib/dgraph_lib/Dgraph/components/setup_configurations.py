"""
Python class to generated Dgraph commands based on configurations.
"""
import json
import pathlib
from subprocess import Popen, PIPE
from robot.api import logger


class DgraphCLI:
    """
    Class to generate the cli-commands based on configurations.
    """

    def __init__(self):
        self.cfg = {}
        self.acl = False
        self.enc = False
        self.enc_file_path = ""
        self.tls = False
        self.tls_mutual = False
        self.tls_mutual_flags = []
        self.details = {}
        self.curr_path = str(pathlib.PurePath(pathlib.Path().absolute()))
        curr_dir = str(pathlib.Path.cwd())
        self.curr_path = curr_dir + "/"
        DgraphCLI.read_config(self)
        self.store_dgraph_details()
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

    def get_enc_file(self):
        """
        Mehtod to get the ENC file path
        :return: enc_flag
        """
        logger.debug(self.curr_path + self.enc_file_path)
        return self.curr_path + self.enc_file_path

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

    def get_cert_from_pem_file(self):
        """
        Method to get certs contained in pem file
        """
        tls_location = self.curr_path + self.cfg['tls']['location']

        # For loading certs into python request handler
        pem_file = "/tls_certs.pem" if self.tls else "/mtls_certs.pem"
        return f"{tls_location}{pem_file}"

    def get_tls_certs(self, cli):
        """
        Method to enabled certificates for tls or mtls configuration
        :return:<mtls_certificates>
        """
        tls_location = self.curr_path + self.cfg['tls']['location']
        tls_cert = ""
        mtls = {}
        if self.tls or self.tls_mutual:
            logger.debug("Appending TLS and mTLS certificates.")
            if self.tls_mutual:
                mtls = {
                    "--tls_cacert": tls_location + "/ca.crt",
                    "--tls_cert": tls_location + "/client.groot.crt",
                    "--tls_key": tls_location + "/client.groot.key",
                }
                if cli == "zero" or cli == "alpha":
                    mtls.update({
                        "--tls_node_cert": tls_location + "/node.crt",
                        "--tls_node_key": tls_location + "/node.key"
                    })
                    verification_type = self.get_mtls_verification_type()
                    tls_cert = tls_cert + f" --tls_client_auth {verification_type} "
                tls_cert = tls_cert + " --tls_internal_port_enabled=true"
            elif self.tls:
                mtls = {
                    "--tls_cacert": tls_location + "/ca.crt",
                }

            for key in mtls:
                tls_cert = tls_cert + f" {key} {str(mtls[key])}"
            if cli == "live":
                tls_cert = tls_cert + f" --tls_server_name \"localhost\""

        logger.debug(tls_cert)
        return tls_cert

    def get_tls_certs_latest(self, cli):
        """
        Method to enabled mtls or tls certs for latest build 21'
        """
        tls_location = self.curr_path + self.cfg['tls']['location']
        tls_cert = ""
        mtls = {}
        if self.tls or self.tls_mutual:
            logger.debug("Appending Latest conf for TLS and mTLS certificates.")
            if self.tls_mutual:
                mtls = {
                    "cacert": tls_location + "/ca.crt",
                    "cert": tls_location + "/client.groot.crt",
                    "key": tls_location + "/client.groot.key"
                }
                if cli == "zero" or cli == "alpha":
                    mtls.update({
                        "node-cert": tls_location + "/node.crt",
                        "node-key": tls_location + "/node.key"
                    })
                    verification_type = self.get_mtls_verification_type()
                    tls_cert = tls_cert + f"client-auth={verification_type};"
            elif self.tls:
                mtls = {
                    "cacert": tls_location + "/ca.crt",
                }
            for key in mtls:
                tls_cert = tls_cert + f"{key}={str(mtls[key])};"
            if self.tls_mutual:
                tls_cert = f"{tls_cert}internal-port-enabled=true"
            if cli == "live":
                tls_cert = tls_cert + f";server-name=\"localhost\""
            tls_cert = f" --tls \"{tls_cert}\""

        logger.debug(tls_cert)
        return tls_cert

    def get_acl_command(self, is_latest):
        """
        Method to enabled acl certs
        :param is_latest: <check_dgraph_version>
        """
        acl_path = self.curr_path + self.cfg['acl']['location']
        logger.debug("Appending acl creds")
        if is_latest:
            acl_conf = f" --acl \"secret-file={acl_path}\""
        else:
            acl_conf = " --acl_secret_file=" + acl_path

        return acl_conf

    @staticmethod
    def get_security_command(is_latest):
        """
        Method to enabled security for whitelist
        :param is_latest: <check_dgraph_version>
        """
        logger.debug("Appending security to whitelist IP's.")
        if is_latest:
            sec = " --security \"whitelist=0.0.0.0/0\""
        else:
            sec = " --whitelist=0.0.0.0/0"

        return sec

    @staticmethod
    def get_ludicrous_command(is_latest):
        """
        Method to enabled ludicrous mode
        :param is_latest: <check_dgraph_version>
        """
        logger.debug("Enabling ludicrous mode in alpha")
        if is_latest:
            ludicrous_mode = " --ludicrous enabled"
        else:
            ludicrous_mode = " --ludicrous_mode"
        return ludicrous_mode

    def get_mtls_verification_type(self):
        """
        Method to get the verification type specified in conf file.
        :return:
        """
        verification_type = None
        logger.debug("getting mtls verification type")
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
            self.enc_file_path = self.cfg['enc']['location']
        if self.cfg['tls']['is_enabled']:
            self.tls = True
        if self.cfg['tls']['mutual_tls']['is_enabled']:
            self.tls_mutual = True

    def build_zero_cli(self, **kwargs):
        """
        Method to generate zero commands based on conf.
        :return:
        """
        cli_name = "zero"
        cli_command = "dgraph " + cli_name + " "
        appender = ""

        is_latest = self.set_dgraph_version()
        # Configure tls and mtls
        if is_latest:
            tls_str = self.get_tls_certs_latest("zero")
        else:
            tls_str = self.get_tls_certs("zero")
        appender = appender + tls_str

        cli_command = cli_command + appender + " 2>&1"
        return cli_command

    def build_alpha_cli(self, bulk_path=None, **kwargs):
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
                                    " -v=2 --zero=localhost:5080"

        is_latest = self.set_dgraph_version()
        cli_command = cli_command + self.get_security_command(is_latest)

        if bulk_path:
            appender = appender + " -p " + bulk_path
        if self.acl:
            appender = appender + self.get_acl_command(is_latest)
        if self.enc:
            enc_path = self.curr_path + self.cfg['enc']['location']
            appender = appender + " --encryption_key_file " + enc_path

        # Configure tls and mtls
        if is_latest:
            tls_str = self.get_tls_certs_latest("alpha")
        else:
            tls_str = self.get_tls_certs("alpha")

        appender = appender + tls_str

        # Enabling ludicrous_mode
        for name, value in kwargs.items():
            if name == "ludicrous_mode" and value == "enabled":
                appender = appender + self.get_ludicrous_command(is_latest)

        cli_command = cli_command + appender + " 2>&1"
        return cli_command

    def store_dgraph_details(self):
        """
        Method to store dgraph version details.
        :return:
        """
        p = Popen(['dgraph', 'version'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
        output, err = p.communicate()
        output = output.split("\n")
        for line in output:
            if ":" in line:
                key = line.split(":")[0].strip()
                value = line.split(":")[1].strip()
                self.details[key] = value
        logger.debug(self.details)

    def get_dgraph_version_details(self, details_key):
        """
        Method to get dgraph version details
        :param details_key: <version details>
            key:
                -   Dgraph version
                -   Branch
        :return: <value>
        """
        return self.details.get(details_key)

    @staticmethod
    def check_version(version_details):
        """
        Method to check the version of dgraph
        :return: <boolean>
        """
        if version_details:
            first = str(version_details).split(".")[0]
            first = first.split("v")[1]
            second = str(version_details).split(".")[1]
            logger.debug(first, second)
            if int(first) == 21:
                return "latest"
            else:
                return "release"
        else:
            logger.debug("Version is empty so considering it as latest dgraph"
                         " from master branch.")
            return True

    def set_dgraph_version(self, version=None, branch=None):
        """
        Method to check and set dgraph version
        """
        if version is None:
            logger.info("dgraph local setup is executed.")
            version = self.get_dgraph_version_details("Dgraph version")
            branch = self.get_dgraph_version_details("Branch")
            is_latest = True if self.check_version(version) == "latest" or branch == "master" or branch == "" \
                else False
        else:
            logger.debug("Dgraph docker setup is executed.")
            is_latest = True if self.check_version(version) == "latest" or branch == "master" \
                else False
        logger.debug(is_latest)
        return is_latest

    @staticmethod
    def get_creds_command_for_acl_login(is_latest, operation="default", username="groot", password="password"):
        """
        Method to get command for Acl login
        :param is_latest: <dgraph_version>
        :param operation: <dgraph command: live, bulk, inc>
        :param username: <acl_username>
        :param password: <acl_password>
        """
        logger.debug(f"is latest: {is_latest}")

        if is_latest:
            cli_live_acl = f" --creds 'user={username};password={password}' "
        else:
            cli_live_acl = f"  -u {username} -p {password} " if operation != "inc" else f"  --user {username}" \
                                                                                        f" --password {password} "

        return cli_live_acl

    def build_loader_command(self, rdf_file, schema_file, loader_type, is_latest_version=None, docker_string=None):
        """
        Method to build bulk/live loader cli command
        :return: live loader cli command
        """

        if is_latest_version:
            is_latest = is_latest_version
        else:
            is_latest = self.set_dgraph_version()

        cli_bulk_encryption = ""

        cli_live_acl = self.get_creds_command_for_acl_login(is_latest)

        loader_type = loader_type.lower()

        cli_command = " dgraph"
        if docker_string:
            cli_command = docker_string + cli_command

        if loader_type == "live":
            cli_command = f"{cli_command} {loader_type} -s {schema_file} " \
                          f"-f " + rdf_file + " -a localhost:9080 -z localhost:5080 "
        elif loader_type == "bulk":
            cli_command = "dgraph " + loader_type + " -s " + schema_file + " -f " + \
                          rdf_file + " --map_shards=2 --reduce_shards=1 --http " \
                                     "localhost:8000 --zero=localhost:5080 "
            if self.enc:
                enc_path = self.curr_path + self.cfg['enc']['location']
                cli_command = cli_command + cli_bulk_encryption + \
                              " --encrypted_out=True --encrypted=False" \
                              " --encryption_key_file " + enc_path
        if self.acl and loader_type != "bulk":
            cli_command = cli_command + cli_live_acl

        if is_latest:
            mtls_certs = self.get_tls_certs_latest("live")
        else:
            mtls_certs = self.get_tls_certs("live")

        cli_command = cli_command + mtls_certs
        return cli_command

    def build_increment_cli_command(self, is_latest_version=None, docker_string=None, alpha_offset: int = 0):
        """
        Method to generate command for increment operation.
        :param alpha_offset: <offset value set for alpha> | default=0
        :param docker_string:
        :param is_latest_version:
        """

        if is_latest_version:
            is_latest = is_latest_version
        else:
            is_latest = self.set_dgraph_version()

        cli_creds_acl = self.get_creds_command_for_acl_login(is_latest, operation="inc")

        if docker_string:
            cli_command = docker_string + " dgraph"
        else:
            cli_command = "dgraph"
        cli_command = f"{cli_command} increment  --alpha localhost:{9080 + alpha_offset} " \
                      f" {cli_creds_acl}"

        if is_latest:
            mtls_certs = self.get_tls_certs_latest("live")
        else:
            mtls_certs = self.get_tls_certs("live")
        cli_command = cli_command + mtls_certs

        return cli_command
