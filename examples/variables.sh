#!/bin/sh

POWERAPI=/opt/PowerAPI
POWERAPI_BIN=$POWERAPI/bin
POWERAPI_LIB=$POWERAPI/lib
ROOT=$1
XML=$2
COUNT=$(echo $* |wc -w)
if [[ $COUNT -lt  2 ]]
then
	echo "Not enough args"
	return
fi

if [[ $COUNT -eq 3 ]]
then
	export POWERAPI_DEBUG=$3
else
	export POWERAPI_DEBUG=0
fi

PATH=$POWERAPI_BIN:$PATH
export LD_LIBRARY_PATH="$POWERAPI_LIB:${LD_LIBRARY_PATH}"
export DYLD_LIBRARY_PATH="$POWERAPI_LIB:${DYLD_LIBRARY_PATH}"
export POWERAPI_CONFIG=$XML
export POWERAPI_ROOT=$ROOT


AGENT_PATH=`pwd`
export PYTHONPATH=$AGENT_PATH/lib/python:$AGENT_PATH/lib/python/Config:$AGENT_PATH/lib/python/Session:$AGENT_PATH/lib/python/Scripts

