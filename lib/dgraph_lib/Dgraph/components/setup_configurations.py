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

    def __init__(self, is_docker=None):
        # declaring variables
        self.cfg = {}
        self.acl = False
        self.enc = False
        self.enc_file_path = ""
        self.tls = False
        self.tls_mutual = False
        self.tls_mutual_flags = []
        self.details = {}
        self.offset = 0
        self.alpha_addr = 0
        self.zero_addr = 0
        self.alpha_server_name = "localhost"
        self.zero_server_name = "localhost"

        # Configuring path to read from config
        self.curr_path = str(pathlib.PurePath(pathlib.Path().absolute()))
        curr_dir = str(pathlib.Path.cwd())
        self.curr_path = curr_dir + "/"
        DgraphCLI.read_config(self)

        # Checking for dgraph version for execution
        if is_docker:
            logger.debug("Execution triggered in docker")
        else:
            logger.debug("Execution triggered in local")
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
        tls_loc = self.cfg["tls"]["location"]
        logger.debug(self.curr_path + tls_loc)
        return self.curr_path + tls_loc

    def get_cert_from_pem_file(self):
        """
        Method to get certs contained in pem file
        """
        tls_location = self.curr_path + self.cfg["tls"]["location"]

        # For loading certs into python request handler
        pem_file = "/tls_certs.pem" if self.tls else "/mtls_certs.pem"
        return f"{tls_location}{pem_file}"

    def get_tls_certs_latest(self, cli, location=None, is_docker=True):
        """
        Method to enabled mtls or tls certs for latest build 21'
        """
        tls_location = f"{self.curr_path}{self.cfg['tls']['location']}"
        if location:
            tls_location = f"{location}{self.cfg['tls']['location']}"

        tls_cert = ""
        mtls = {}
        if self.tls or self.tls_mutual:
            logger.debug("Appending Latest conf for TLS and mTLS certificates.")
            if self.tls_mutual:
                mtls = {
                    "ca-cert": tls_location + "/ca.crt",
                    "client-cert": tls_location + "/client.groot.crt",
                    "client-key": tls_location + "/client.groot.key",
                }
                if cli == "zero" or cli == "alpha":
                    mtls.update(
                        {
                            "server-cert": tls_location + "/node.crt",
                            "server-key": tls_location + "/node.key",
                        }
                    )
                    verification_type = self.get_mtls_verification_type()
                    tls_cert = tls_cert + f"client-auth-type={verification_type};"
            elif self.tls:
                mtls = {
                    "ca-cert": tls_location + "/ca.crt",
                }
            for key in mtls:
                tls_cert = tls_cert + f"{key}={str(mtls[key])};"
            if self.tls_mutual:
                tls_cert = f"{tls_cert}internal-port=true"
            if cli == "live":
                tls_cert = tls_cert + f';server-name="localhost"'

            if is_docker:
                tls_cert = f' --tls="{tls_cert}"'
            else:
                tls_cert = f' --tls "{tls_cert}"'

        logger.debug(tls_cert)
        return tls_cert

    def get_mtls_verification_type(self):
        """
        Method to get the verification type specified in conf file.
        :return:
        """
        verification_type = None
        logger.debug("getting mtls verification type")
        for key in self.cfg["tls"]["mutual_tls"]:
            if self.cfg["tls"]["mutual_tls"][key] and key != "is_enabled":
                verification_type = key
        return verification_type

    # Verification checks based on dgraph version
    def get_acl_command(self):
        """
        Method to enabled acl certs
        """
        acl_path = self.curr_path + self.cfg["acl"]["location"]
        logger.debug("Appending acl creds")
        acl_conf = f' --acl "secret-file={acl_path}"'
        return acl_conf

    @staticmethod
    def get_security_command():
        """
        Method to enabled security for whitelist
        """
        logger.debug("Appending security to whitelist IP's.")
        sec = ' --security "whitelist=0.0.0.0/0"'
        return sec

    def get_encryption_command(self):
        """
        Method to enable encryption
        """
        logger.debug("Appending encryption..")
        enc_path = self.curr_path + self.cfg["enc"]["location"]
        enc = f' --encryption "key-file={enc_path};" '
        return enc

    @staticmethod
    def get_cache_command():
        """
        Method to append cache size
        """
        logger.debug("Appending Cache..")
        cache = f' --cache "size-mb=6000" '
        return cache

    @staticmethod
    def get_ludicrous_command():
        """
        Method to enabled ludicrous mode
        """
        logger.debug("Enabling ludicrous mode in alpha")
        ludicrous_mode = ' --ludicrous "enabled=true"'
        return ludicrous_mode

    def get_creds_command_for_acl_login(
        self, operation="default", username="groot", password="password"
    ):
        """
        Method to get command for Acl login
        :param operation: <dgraph command: live, bulk, inc>
        :param username: <acl_username>
        :param password: <acl_password>
        """
        acl_appender = ""
        if self.acl:
            acl_appender = f" --creds 'user={username};password={password}' "
        return acl_appender

    def read_config(self):
        """
        Method to set the configurations based on conf/dgraph/conf_dgraph.json
        :return:
        """
        conf_path = self.curr_path + "conf/dgraph/conf_dgraph.json"
        logger.info("configuration path: " + conf_path)
        with open(conf_path) as conf_file:
            self.cfg = json.load(conf_file)
        self.offset = self.cfg["offset"]
        self.alpha_addr = self.cfg["alpha"]["addr"]
        self.alpha_server_name = self.cfg["alpha"]["server"]
        self.zero_addr = self.cfg["zero"]["addr"]
        self.zero_server_name = self.cfg["zero"]["server"]
        if self.cfg["acl"]["is_enabled"]:
            self.acl = True
        if self.cfg["enc"]["is_enabled"]:
            self.enc = True
            self.enc_file_path = self.cfg["enc"]["location"]
        if self.cfg["tls"]["is_enabled"]:
            self.tls = True
        if self.cfg["tls"]["mutual_tls"]["is_enabled"]:
            self.tls_mutual = True

    def store_dgraph_details(self):
        """
        Method to store dgraph version details.
        :return:
        """
        p = Popen(
            ["dgraph", "version"],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf-8",
        )
        output, err = p.communicate()
        output = output.split("\n")
        for line in output:
            if ":" in line:
                key = line.split(":")[0].strip()
                value = line.split(":")[1].strip()
                self.details[key] = value
        logger.debug(self.details)

    def store_dgraph_details_docker(self, docker_string):
        """
        Method to store dgraph version details.
        :return:
        """
        p = Popen(
            f"{docker_string} dgraph version",
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            encoding="utf-8",
            shell=True,
        )
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
        logger.debug(self.details.get(details_key))
        return self.details.get(details_key)

    def build_zero_cli(self, offset=None, **kwargs):
        """
        Method to generate zero commands based on conf.
        :param offset:
        :param kwargs:
            offset: offset value to initialize dgraph
        :return:
        """
        cli_name = "zero"
        cli_command = f"dgraph {cli_name} --replicas 3  "
        appender = ""
        args_appender = ""
        logger.debug(f"offset value: {self.offset}")
        args_appender = args_appender + f" -o {self.offset}"

        # Configure tls and mtls
        tls_str = self.get_tls_certs_latest("zero")
        appender = appender + tls_str
        appender = appender + args_appender

        cli_command = cli_command + appender + " 2>&1"
        return cli_command

    def build_docker_zero_and_alpha_cli_command(
        self,
        container_name,
        dgraph_version,
        zero_count=1,
        alpha_count=1,
        ludicrous_mode=False,
        bulk_path=None,
    ):
        """
        Method to build zero and alpha cli command for docker
        :param bulk_path:
        :param alpha_count:
        :param zero_count: No of alpha's
        :param container_name: name of the docker container
        :param dgraph_version: dgraph version of the docker build

        :return:
        """
        logger.debug(dgraph_version)
        appenders = ""
        extra_alpha_flags = []
        extra_zero_flags = []
        alpha_mounts = []
        zero_mounts = []
        zero_mounts.append(f"{self.curr_path}results:{self.curr_path}results")

        alpha_mounts.append(
            f"{self.curr_path}test_data/datasets:{self.curr_path}test_data/datasets"
        )
        alpha_mounts.append(f"{self.curr_path}export:{self.curr_path}export")
        alpha_mounts.append(f"{self.curr_path}backup:{self.curr_path}backup")
        alpha_mounts.append(f"{self.curr_path}results:{self.curr_path}results")

        if self.acl:
            appenders = (
                f" --acl_secret {self.curr_path}conf/dgraph/acl/hmac_secret_file "
            )
            alpha_mounts.append(
                f"{self.curr_path}conf/dgraph/acl/hmac_secret_file:{self.curr_path}conf/dgraph/acl/hmac_secret_file"
            )
        if self.enc:
            extra_alpha_flags.append(str(self.get_encryption_command()).strip())
            alpha_mounts.append(
                f"{self.curr_path}conf/dgraph/encryption:{self.curr_path}conf/dgraph/encryption"
            )

        if ludicrous_mode:
            appenders += " --ludicrous"

        if bulk_path:
            extra_alpha_flags.append(f"-p={bulk_path}")

        tls_alpha_str = ""
        tls_zero_str = ""
        if self.tls and self.tls_mutual:
            alpha_mounts.append(
                f"{self.curr_path}conf/dgraph/mTLS/tls:{self.curr_path}conf/dgraph/mTLS/tls:ro"
            )
            zero_mounts.append(
                f"{self.curr_path}conf/dgraph/mTLS/tls:{self.curr_path}conf/dgraph/mTLS/tls:ro"
            )
            tls_zero_str = self.get_tls_certs_latest("zero", is_docker=True)
            tls_alpha_str = self.get_tls_certs_latest("alpha", is_docker=True)
            extra_alpha_flags.append(f"{tls_alpha_str}")
            extra_zero_flags.append(f"{tls_zero_str}")

        alpha_flags = ""
        for flag in extra_alpha_flags:
            alpha_flags += f" {flag}"

        zero_flags = ""
        for flag in extra_zero_flags:
            zero_flags += f"{flag}"

        appenders += (
            f" --extra_alpha_flags='{alpha_flags}'  --extra_zero_flags='{zero_flags}'"
        )

        alpha_volumes = ""
        for mount in alpha_mounts:
            alpha_volumes += f" --alpha_volume {mount}"

        zero_volumes = ""
        for mount in zero_mounts:
            zero_volumes += f" --zero_volume {mount}"
        docker_command = f"compose --data_dir={self.curr_path}results --user -l=false {alpha_volumes} {zero_volumes} -z={zero_count} -a={alpha_count} {appenders} -o={self.offset} -t={dgraph_version} --out={self.curr_path}results/docker-compose.yml "
        return docker_command

    def build_alpha_cli(
        self,
        bulk_path=None,
        offset: int = 0,
        learner=False,
        zero_address=None,
        cwd=None,
        group=1,
        **kwargs,
    ):
        """
        Method to generate alpha commands based on conf.
        \n accepts one param for bulk data initializing
        :param zero_address:
        :param offset:
        :param bulk_path: <bulk loader data path>
        :return:
        """

        cli_name = "alpha"
        appender = ""
        args_appender = ""

        if cwd:
            appender += f" --cwd {cwd}"
        if offset == 0:
            offset = self.offset

        raft_appender = f' --raft "group={group};learner={learner}" '
        appender += raft_appender
        if learner:
            offset += 1
        logger.debug(f"offset value: {offset}")
        args_appender = args_appender + f" -o {offset}"
        for key, value in kwargs.items():
            if key == "ludicrous_mode" and value == "enabled":
                args_appender = args_appender + self.get_ludicrous_command()

        if zero_address:
            cli_command = (
                f"dgraph {cli_name} {self.get_cache_command()} "
                f"--zero={self.zero_server_name}:{zero_address}"
            )
        else:
            cli_command = (
                f"dgraph {cli_name} {self.get_cache_command()} "
                f"--zero={self.zero_server_name}:{self.zero_addr}"
            )

        cli_command = cli_command + self.get_security_command()

        if bulk_path:
            appender = appender + f' --postings "{bulk_path}" '
        if self.acl:
            appender = appender + self.get_acl_command()
        if self.enc:
            appender = appender + self.get_encryption_command()

        # Configure tls and mtls
        tls_str = self.get_tls_certs_latest("alpha")

        appender = appender + tls_str

        appender = appender + args_appender

        cli_command = cli_command + appender + "  -v=2  2>&1"
        return cli_command

    def build_loader_command(
        self,
        rdf_file,
        schema_file,
        loader_type,
        docker_string=None,
        is_learner=None,
        zero_host_name=None,
        alpha_host_name=None,
        zero_address=None,
        alpha_address=None,
        out_dir=None,
    ):
        """
        Method to build bulk/live loader cli command
        :param rdf_file: <rdf_data_file>
        :param schema_file: <schema_file>
        :param loader_type: <live\bulk>
        :param docker_string: <docker exec string>
        :return: live loader cli command
        """

        # Loader CLI command generation
        cli_command = " dgraph"
        cli_bulk_encryption = ""
        logger.debug(f"offset value: {self.offset}")
        loader_type = loader_type.lower()
        docker_location = None
        if docker_string:
            logger.debug("Appending docker string")
            cli_command = docker_string + cli_command
            self.store_dgraph_details_docker(docker_string)

        if zero_host_name is None:
            zero_host_name = self.zero_server_name

        if zero_address is None:
            zero_address = self.zero_addr

        if alpha_host_name is None:
            alpha_host_name = self.alpha_server_name

        if alpha_address is None:
            alpha_address = self.alpha_addr

        if is_learner:
            if alpha_address:
                alpha_address += 1
            else:
                alpha_address = self.alpha_addr + 1

        # Building command for live loader
        if loader_type == "live":
            cli_command = (
                f"{cli_command} {loader_type} -s {schema_file} "
                f"-f {rdf_file} -a {alpha_host_name}:{alpha_address} "
                f"-z {zero_host_name}:{zero_address} "
            )
            branch = self.get_dgraph_version_details("Branch")
            if branch == "master":
                cli_command += " --force-namespace 0"

        # Building command for bulk loader
        elif loader_type == "bulk":
            cli_command = (
                f"{cli_command} {loader_type} -s {schema_file} -f {rdf_file} "
                f"--map_shards=2 --reduce_shards=1 "
                f"--http localhost:{8000 + self.offset}"
                f" --zero={zero_host_name}:{zero_address} "
            )

            if out_dir:
                cli_command += f" --out={out_dir}"

            if self.enc:
                cli_command = (
                    cli_command
                    + cli_bulk_encryption
                    + f" --encrypted_out=True --encrypted=False"
                    f" {self.get_encryption_command()}"
                )

        # Fetch ACL args based on configuration
        if self.acl and loader_type != "bulk":
            cli_live_acl = self.get_creds_command_for_acl_login()
            cli_command = cli_command + cli_live_acl

        # Fetching latest tls args based on configuration
        mtls_certs = self.get_tls_certs_latest("live", location=docker_location)

        cli_command = cli_command + mtls_certs + " -v 2 "
        return cli_command

    def build_increment_cli_command(
        self,
        docker_string=None,
        alpha_host_name=None,
        alpha_address=None,
    ):
        """
        Method to generate command for increment operation.
        :param alpha_offset: <offset value set for alpha> | default=0
        :param docker_string: <docker exec string>
        """

        # Increment CLI command generation
        cli_creds_acl = self.get_creds_command_for_acl_login()

        if alpha_host_name is None:
            alpha_host_name = self.alpha_server_name

        if alpha_address is None:
            alpha_address = self.alpha_addr

        docker_location = None
        if docker_string:
            cli_command = docker_string + " dgraph"
        else:
            cli_command = "dgraph"
        cli_command = (
            f"{cli_command} increment  --alpha {alpha_host_name}:{alpha_address} "
            f" {cli_creds_acl}"
        )

        # Fetching latest tls args based on configuration
        mtls_certs = self.get_tls_certs_latest("live", location=docker_location)

        cli_command = cli_command + mtls_certs

        return cli_command
