#!/bin/bash

# @author: Sourav Mukherjee
# @date: 3/1/2021
# This script is used to do thw following:
#   1. Install virtualenv.
#   2. Activate virtualenv.
#   3. Install dependencies in virtualenv.
#   4. Run robot test.
#   5. Deactivate the virtualenv.

usage() {
    echo "Usage: $0 [-l <Dgraph|Slash>] [-c <disabled|enabled>]"
}

while getopts ":l:c:" o; do
    case "${o}" in
        l)
            l=${OPTARG}
            if [[ ${l} == "Dgraph" || ${l} == "Slash" ]]; then 
            args="-l "${l} 
            else
                usage
                exit 1
            fi
            ;;
        c)
            c=${OPTARG}
            if [[ ${c} == "disabled" || ${c} == "enabled" ]]; then
                args+=" -c "${c} 
            else
                usage
                exit 1
            fi
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${l}" ] || [ -z "${c}" ]; then
    usage
    exit 1
fi

epoch=`date +%s`
pip3 install virtualenv==20.2.2
python3 -m venv env_${epoch}
source env_${epoch}/bin/activate
pwd
echo "Virtual environment used: $VIRTUAL_ENV" 
echo "Args been set: ${args}"
python3 env_setup.py -l ${l} -c ${c}
echo "------------ Running Test --------------"
cd ..
echo "Current directory: " $PWD 
robot test_suites/dgraph/Linux/dgraph_suite.robot
deactivate