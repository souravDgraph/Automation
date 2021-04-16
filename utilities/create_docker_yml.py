import getopt
import json
import pathlib
import sys
import logging
import yaml


def main(argv):
    """
    Method to setup the docker-compose file
    """
    try:
        opts, args = getopt.getopt(argv, "hc:v:", ["config=", "version="])
        logging.debug(args)
        if not opts:
            print('Usage: python/python3 create_docker_yml.py -v <version> -c <configuration>'
                  + '\n -v master -c enabled | disabled')
            sys.exit(2)
    except getopt.GetoptError:
        print('Usage: python/python3 create_docker_yml.py -v <version> -c <configuration>' +
              '\n -v master -c enabled | disabled')
        sys.exit(2)

    for opt, arg_value in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            version = arg_value
        elif opt in ("-c", "--config"):
            confg = arg_value
        else:
            usage()
            raise (Exception("invalid argument for the setup process "
                             "Dgraph please also add the configuration argument."))
    try:
        generate_config(version, confg)
    except UnboundLocalError as e:
        raise (UnboundLocalError("invalid argument for the setup process try -h for usage"))


def generate_config(version, confg):
    """
    Method to generate the docker-compose file based on requirement.
    :param version: <branch_name>
    :param confg: <enabled | disabled>
    :return:
    """
    if confg not in ['enabled', 'disabled']:
        raise Exception("Configuration not enabled check if there is a typo\n"
                        " input for configuration: " + confg)
    if confg == "enabled":
        create_docker_compose_file(alphas=3, is_configured=True, version=version)
        create_docker_compose_file(alphas=1, is_configured=True, version=version)

    elif confg == "disabled":
        create_docker_compose_file(alphas=3, is_configured=False, version=version)
        create_docker_compose_file(alphas=1, is_configured=False, version=version)


def usage():
    """
    Method to define the usage of the code from command line.
    :return:
    """
    usage_text = """
        Usage:
        python/python3 create_docker_yml.py -v <version> -c <configuration>
            version = master | v20.11.2, configuration = enabled | disabled
        EX:     
        python/python3 create_docker_yml.py -v master -c enabled
    """
    print(usage_text)


def create_docker_compose_file(zeros: int = 1, alphas: int = 1, is_configured: bool = False, version="master"):
    # Creating Zero container
    curr_dir = str(pathlib.Path.cwd())
    curr_path = curr_dir + '/'
    export_path = curr_path + "../export"
    backup_path = curr_path + "../backup"
    working_dir = curr_path + "../results"
    with open(curr_path + '../conf/dgraph/conf_dgraph.json') as dg_conf_file:
        dgraph_conf = json.load(dg_conf_file)
    off_set_value = dgraph_conf['offset']
    services = {}
    zero_services = {}
    zero_command = f'dgraph zero --my=zero0:{5080 + off_set_value} --logtostderr -v=2 -o {off_set_value} '
    dgraph_version = f"dgraph/dgraph:{version}"
    if is_configured:
        zero_command = zero_command + ' --bindall '

        tls_command = build_tls_command('/dgraph-tls/') + ' --tls_client_auth VERIFYIFGIVEN' \
                                                          '  --tls_internal_port_enabled=true'
        zero_command = zero_command + " " + tls_command

    for zero_count in range(zeros):
        zero_configs = []
        zero_name = 'zero' + str(zero_count)
        if is_configured:
            zero_configs = [{
                "type": "bind",
                "source": "../../../Automation",
                "target": "/Automation",
                "read_only": True
            }, {
                "type": "bind",
                "source": export_path,
                "target": export_path,
                "read_only": False
            },
                {
                    "type": "bind",
                    "source": backup_path,
                    "target": backup_path,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": working_dir,
                    "target": working_dir,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": "../dgraph/mTLS/tls/",
                    "target": "/dgraph-tls/",
                    "read_only": True
                }]
        else:
            zero_configs = [
                {
                    "type": "bind",
                    "source": "../../../Automation",
                    "target": "/Automation",
                    "read_only": True
                },
                {
                    "type": "bind",
                    "source": export_path,
                    "target": export_path,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": backup_path,
                    "target": backup_path,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": working_dir,
                    "target": working_dir,
                    "read_only": False
                }
            ]
        opening_port = 5080 + off_set_value
        closing_port = 6080 + off_set_value
        zero_services = {zero_name:
                             {'image': dgraph_version, 'working_dir': f'{working_dir}/{zero_name}',
                              'ports': [f"{opening_port}:{opening_port}", f"{closing_port}:{closing_port}"],
                              'volumes': zero_configs,
                              'labels': {'cluster': 'test',
                                         'service': 'zero'},
                              'command': zero_command}}
    services.update(zero_services)

    # Creating Alpha container
    alpha_command = 'dgraph alpha  --logtostderr -v=2 ' \
                    '--whitelist=0.0.0.0/0'
    if is_configured:
        enc_command = ' --encryption_key_file /dgraph-enc/enc_key_file '
        alc_command = ' --acl_secret_file /dgraph-acl/hmac_secret_file '
        tls_command = build_tls_command('/dgraph-tls/') + ' --tls_client_auth VERIFYIFGIVEN' \
                                                          '  --tls_internal_port_enabled=true '
        alpha_command = alpha_command + enc_command + alc_command + tls_command

    for alpha_count in range(alphas):
        final_alpha_command = ""
        port = 7080 + off_set_value
        alpha_volumes = []
        ports_list = []
        opening_port = 8080 + off_set_value
        closing_port = 9080 + off_set_value
        ports_list.append(f"{opening_port}:{opening_port}")
        ports_list.append(f"{closing_port}:{closing_port}")
        if off_set_value != 0:
            alpha_name = 'alpha' + str(alpha_count) + f' -o {off_set_value}'
        alpha_name = 'alpha' + str(alpha_count)
        if alpha_count >= 1:
            ports_list.clear()
            off_set_value = 100 + off_set_value
            port = port + off_set_value
            opening_port = opening_port + off_set_value
            closing_port = closing_port + off_set_value
            ports_list.append(f"{opening_port}:{opening_port}")
            ports_list.append(f"{closing_port}:{closing_port}")
            alpha_command = alpha_command + " -o " + str(off_set_value)
        final_alpha_command = alpha_command + ' --my=' + alpha_name + ':' + str(port) + \
                              f' --zero=zero0:{5080 + off_set_value} -o {off_set_value} '
        if is_configured:
            alpha_volumes = [
                {
                    "type": "bind",
                    "source": "../../../Automation",
                    "target": "/Automation",
                    "read_only": True
                }, {
                    "type": "bind",
                    "source": "../dgraph/acl",
                    "target": "/dgraph-acl/",
                    "read_only": True
                },
                {
                    "type": "bind",
                    "source": working_dir,
                    "target": working_dir,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": export_path,
                    "target": export_path,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": backup_path,
                    "target": backup_path,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": "../dgraph/encryption/",
                    "target": "/dgraph-enc/",
                    "read_only": True
                },
                {
                    "type": "bind",
                    "source": "../dgraph/mTLS/tls/",
                    "target": "/dgraph-tls/",
                    "read_only": True
                }
            ]
        else:
            alpha_volumes = [
                {
                    "type": "bind",
                    "source": "../../../Automation",
                    "target": "/Automation",
                    "read_only": True
                },
                {
                    "type": "bind",
                    "source": working_dir,
                    "target": working_dir,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": export_path,
                    "target": export_path,
                    "read_only": False
                },
                {
                    "type": "bind",
                    "source": backup_path,
                    "target": backup_path,
                    "read_only": False
                }
            ]
        alpha_services = {alpha_name: {
            "image": dgraph_version,
            "working_dir": f"{working_dir}/{alpha_name}",
            "volumes": alpha_volumes,
            "ports": ports_list,
            "labels": {
                "cluster": "test",
                "service": "alpha"
            },
            "command": final_alpha_command
        }}
        services.update(alpha_services)

    # Appending zero and alpha containers
    dict_file = {'version': '3.2', 'services': services}
    if alphas == 1:
        dir_name = 2
    else:
        dir_name = 4
    with open(r'../conf/docker-' + str(dir_name) + 'node/docker-compose.yml', 'w') as compose_file:
        yaml.dump(dict_file, compose_file)
        print("Successfully generated YAML file for docker")


def build_tls_command(tls_location):
    certs = {
        "--tls_cacert": tls_location + "ca.crt",
        "--tls_cert": tls_location + "client.groot.crt",
        "--tls_key": tls_location + "client.groot.key",
        "--tls_node_cert": tls_location + "node.crt",
        "--tls_node_key": tls_location + "node.key"
    }
    tls_conf = ""
    for cert in certs:
        tls_conf = tls_conf + " " + cert + " " + str(certs[cert])
    return tls_conf


if __name__ == "__main__":
    main(sys.argv[1:])
