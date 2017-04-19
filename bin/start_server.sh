#!/bin/sh
SCRIPT_PATH=$(dirname $0)
ROOT=$SCRIPT_PATH/..

export PYTHONPATH=${ROOT}/lib/python:${ROOT}/lib/python/Config:${ROOT}/lib/python/Session
python ${ROOT}/lib/python/agent/agent.py
