import getopt
import logging
import pathlib
import platform
import subprocess
import sys


def main(argv):
    # Method to install all the package dependencies and lib based on the req
    # Usage: python/python3 env_setup.py -l <proj_name>
    proj_name = ''
    try:
        opts, args = getopt.getopt(argv, "hl:",  "lib=")
        if not opts:
            print('Usage: python/python3 env_setup.py -l <proj_name>' + '\n proj_name = Dgraph, Slash')
            sys.exit(2)
    except getopt.GetoptError:
        print('Usage: python/python3 env_setup.py -l <proj_name>' + '\n proj_name = Dgraph, Slash')
        sys.exit(2)

    for opt, arg_value in opts:
        if opt == '-h':
            print('Usage: python/python3 env_setup.py -l <proj_name>' + '\n proj_name = Dgraph, Slash')
            sys.exit()
        elif opt in ("-l", "--lib"):
            platform_name = platform.system()
            if platform_name == 'Windows':
                pip_name = 'pip'
                python_name = 'python'
            else:
                pip_name = 'pip3'
                python_name = 'python3'

            subprocess.check_call([pip_name, 'install', '-r', '../requirements.txt'])
            if proj_name == "Dgraph":
                proj_lib_paths = ['./lib/dgraph_lib/']
            elif proj_name == "Slash":
                proj_lib_paths = ['./lib/selenium_client/',
                             './lib/slash_ui_library/']
            print("\n\n\n*********Installing Lib for: " + proj_name+" *****************\n\n\n")
            cwd_path = pathlib.PurePath(pathlib.Path().absolute(), '../')

            # installing all the custom libraries...
            for lib_path in proj_lib_paths:
                cur_lib_path = cwd_path.joinpath(lib_path)
                subprocess.check_call([python_name, 'setup.py', 'install'], cwd=cur_lib_path)


if __name__ == "__main__":
    main(sys.argv[1:])

