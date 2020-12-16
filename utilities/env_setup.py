import subprocess
import pathlib
import platform
import  logging

# implement pip as a subprocess:
platform_name = platform.system()

if platform_name == 'Windows':
    pip_name = 'pip'
    python_name = 'python'
else:
    pip_name = 'pip3'
    python_name = 'python3'

subprocess.check_call([pip_name, 'install', '-r', '../requirements.txt'])
paths = ['./lib/dgraph_lib/', './lib/slash_selenium_library/',
         './lib/slash_ui_library/']
cwd = pathlib.Path().absolute()
cwd = pathlib.PurePath(cwd, '../')

# installing all the custom libraries...
for path in paths:
    lib_path = cwd.joinpath(path)
    logging.info(lib_path)
    subprocess.check_call([python_name, 'setup.py', 'install'],  cwd=lib_path)
