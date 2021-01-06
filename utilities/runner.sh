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
    echo "Usage: $0 [-l <Dgraph|Slash>] [-c <disabled|enabled>] [-t <absolute path of test suite>]"
}

# Getting all the required options
while getopts ":l:c:t:" o; do
    case "${o}" in
        l)
            l=${OPTARG}
            if [[ ${l} == "Dgraph" || ${l} == "Slash" ]]; then 
            args="-l "${l} 
            else
                usage
                echo 1
                exit 1
            fi
            ;;
        c)
            c=${OPTARG}
            if [[ ${c} == "disabled" || ${c} == "enabled" ]]; then
                args+=" -c "${c} 
            else
                usage
                echo 11
                exit 1
            fi
            ;;
        t)
            t=${OPTARG}
            args+=" -t "${t} 
            ;;
        *)
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${l}" ] || [ -z "${c}" ] || [ -z "${t}" ]; then
    usage
    echo 1111
    exit 1
fi

# Activating the virtualenv and running automation
epoch=`date +%s`
pip3 install virtualenv==20.2.2
python3 -m venv env_${epoch}
source env_${epoch}/bin/activate
pwd
echo "Virtual environment used: $VIRTUAL_ENV" 
echo "Args been set: ${args}"
python3 env_setup.py -l ${l} -c ${c}
echo "------------ Running Test ${t} --------------"
cd ..
echo "Current directory: " $PWD 
robot ${t}
deactivate