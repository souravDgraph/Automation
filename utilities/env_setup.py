"""
Environment setup file for configuring the framework before execution.
"""
import getopt
import json
import pathlib
import platform
import subprocess
import logging
import sys

# pylint: disable=C0301


def main(argv):
    """
    Method to install all the package dependencies and lib based on the req
    Usage: python/python3 env_setup.py -l <proj_name>
     project name =  Dgraph | Slash
    :param argv:
    :return:
    """
    try:
        opts, args = getopt.getopt(argv, "hl:c:", ["lib=", "conf="])
        logging.debug(args)
        if not opts:
            print('Usage: python/python3 env_setup.py -l <proj_name>'
                  + '\n proj_name = All, Dgraph, Slash, Common, CustomTestRailListener')
            sys.exit(2)
    except getopt.GetoptError:
        print('Usage: python/python3 env_setup.py -l <proj_name>' +
              '\n proj_name = All, Dgraph, Slash, Common, CustomTestRailListener')
        sys.exit(2)

    dgraph_check = False
    conf_check = False
    for opt, arg_value in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-l", "--lib"):
            if arg_value.lower() == "dgraph" or arg_value.lower() == "all":
                dgraph_check = True
            setup_lib(arg_value)
        elif opt in ("-c", "--config"):
            if dgraph_check:
                conf_check = True
                generate_config(arg_value)
    if dgraph_check:
        if not conf_check:
            usage()
            raise (Exception("invalid argument for the setup process "
                             "Dgraph please also add the configuration argument."))


def usage():
    """
    Method to define the usage of the code from command line.
    :return:
    """
    print("Usage:\n")
    print('python/python3 env_setup.py -l <proj_name> -c <configuration>'
          + '\n proj_name = All, CustomTestRailListener, Dgraph | Slash | Common,'
            ' configuration = enabled | disabled')
    print('')
    print('Ex: python/python3 env_setup.py -l All -c enabled'
          + '\n proj_name = All, config = enabled|disabled.')
    print('')
    print('Ex: python/python3 env_setup.py -l Dgraph -c enabled'
          + '\n proj_name = Dgraph, config = enabled|disabled.')
    print('')
    print('Ex: python/python3 env_setup.py -l Slash'
          + '\n proj_name = Slash')
    print('')
    print('Ex: python/python3 env_setup.py -l Common'
          + '\n proj_name = Common')
    print('')
    print('Ex: python/python3 env_setup.py -l CustomTestRailListener'
          + '\n proj_name = CustomTestRailListener')


def generate_config(arg_value):
    """
    Method to generate the config file based on requirement.
    :param arg_value:
    :return:
    """
    if arg_value not in ['enabled', 'disabled']:
        raise Exception("Configuration not enabled check if there is a typo\n"
                        " input for configuration: " + arg_value)
    conf = {
        "acl": {
            "is_enabled": True,
            "location": "conf/dgraph/acl/hmac_secret_file"
        },
        "enc": {
            "is_enabled": True,
            "location": "conf/dgraph/encryption/enc_key_file"
        },

        "tls": {
            "is_enabled": True,
            "mutual_tls": {
                "is_enabled": True,
                "REQUEST": False,
                "REQUIREANY": False,
                "VERIFYIFGIVEN": True,
                "REQUIREANDVERIFY": False
            },
            "force_tls": False,
            "location": "conf/dgraph/mTLS/tls"
        }
    }
    if arg_value == "enabled":
        with open('../conf/dgraph/conf_dgraph.json', 'w') as outfile:
            json.dump(conf, outfile, indent=4)
    elif arg_value == "disabled":
        conf["acl"]["is_enabled"] = False
        conf["enc"]["is_enabled"] = False
        conf["tls"]["is_enabled"] = False
        conf["tls"]["mutual_tls"]["is_enabled"] = False
        conf["tls"]["mutual_tls"]["VERIFYIFGIVEN"] = False
        with open('../conf/dgraph/conf_dgraph.json', 'w') as outfile:
            json.dump(conf, outfile, indent=4)


def setup_lib(proj_name):
    """
    Method to setup the lib.
    :param proj_name:
    :return:
    """
    platform_name = platform.system()
    if platform_name == 'Windows':
        pip_name = 'pip'
        python_name = 'python'
    else:
        pip_name = 'pip3'
        python_name = 'python3'

    subprocess.check_call([pip_name, 'install', '-r', '../requirements.txt'])
    proj_lib_paths = []
    if proj_name.lower() == "dgraph":
        proj_lib_paths = ['./lib/dgraph_lib/']
    elif proj_name.lower() == "slash":
        proj_lib_paths = ['./lib/selenium_client/',
                          './lib/slash_ui_library/',
                          './lib/slash_api_library/',
                          './lib/slash_cli_library/',
                          './lib/requests_client']
    elif proj_name.lower() == "common":
        proj_lib_paths = ['./lib/common_lib/']
    elif proj_name.lower() == "customtestraillistener":
        proj_lib_paths = ['./lib/test_rail_listener_lib/']
    elif proj_name.lower() == "all":
        proj_lib_paths = ['./lib/dgraph_lib/', './lib/selenium_client/', './lib/slash_ui_library/',
                          './lib/slash_api_library/', './lib/requests_client', './lib/common_lib/', 
                          './lib/slash_cli_library/', './lib/test_rail_listener_lib/']
        proj_name = "Dgraph, Slash, Common, Test Rails Listener"

    print("\n\n\n*********Installing Lib for: " + proj_name + " *****************\n\n\n")
    cwd_path = pathlib.PurePath(pathlib.Path().absolute(), '../')
    print("cwd -- " + str(cwd_path))
    # installing all the custom libraries...
    for lib_path in proj_lib_paths:
        cur_lib_path = cwd_path.joinpath(lib_path)
        print("Installing -- " + str(cur_lib_path))
        try:
            subprocess.check_call([python_name, 'setup.py', 'install'], cwd=cur_lib_path)
        except:
            print("Skipping " + str(cur_lib_path))


if __name__ == "__main__":
    main(sys.argv[1:])
