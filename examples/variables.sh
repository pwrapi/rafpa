#!/bin/sh

POWERAPI=/opt/PowerAPI
POWERAPI_BIN=$POWERAPI/bin
POWERAPI_LIB=$POWERAPI/lib
ROOT=$0
XML=$1
COUNT=$(echo $* |wc -w)
echo $COUNT
if [[ $COUNT -lt  2 ]]
then
	echo "Not enough args"
	exit 1
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
