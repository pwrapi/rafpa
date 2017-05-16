#!/bin/sh
SCRIPT_PATH=$(dirname $0)
ROOT=$SCRIPT_PATH/..

export PYTHONPATH=${ROOT}/lib/python
python ${ROOT}/lib/python/agent.py
