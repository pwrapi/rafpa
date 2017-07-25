#!/bin/sh
SCRIPT_PATH=$(dirname $0)
ROOT=$SCRIPT_PATH/..
#export REDFISH_AGENT_ROOT=$ROOT
export PYTHONPATH=${ROOT}/lib/python
#python ${ROOT}/lib/python/proxy.py
python ${ROOT}/lib/python/myDaemon.py $1
