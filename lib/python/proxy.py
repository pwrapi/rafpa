# Copyright 2017 Hewlett Packard Enterprise Development LP
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may
# be used to endorse or promote products derived from this software without specific
# prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,WHETHER IN
# CONTRACT,STRICT LIABILITY,OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from Connection import Connection
import signal
import Util
import os
import sys
from Log import Logger,Log  
from ExceptionCollection import ConfigError, ConfigPathError, SessionCreateError


log = None

loop = 1
port = 8080
def register_signals():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    signal.signal(signal.SIGFPE, signal_handler)
    signal.signal(signal.SIGILL, signal_handler)
    signal.signal(signal.SIGSEGV, signal_handler)

def signal_handler(signum, frame):
    global loop	
    log.Info("Received signal {signo}. Stopping!!".format(signo=signum))
    loop = 0


def load_config():
    # CONFIG_PATH from Environment

    config_path = Util.get_config_path()
    Util.LoadConfiguration(config_path)
    log.Info("Successfully Loaded Configuration database ..")
    sys.path.insert(0, Util.get_scripts_path())

    # Get all server_types
    configobj = Util.getConfigObj()
    server_types_names = configobj.keys()
    for a_type_name in server_types_names:
        log.Info("Handling {0}".format(a_type_name))
        a_type_devices = configobj[a_type_name]
        for device_name in a_type_devices.keys():
            device = a_type_devices[device_name]
            attr_names = device.keys()
            for attr_name in attr_names:
                log.Info("Handling \"{0}\" device \"{1}\" attribute \"{2}\"".format(a_type_name,device_name, attr_name))
                attr = device[attr_name]
                attr.load(device)

def load_sessions():

    config_path = Util.get_config_path()
    Util.LoadSessions(config_path)
    nodenames = Util.getNodeNames()
    nodesobj = Util.getNodesobj()
    for nodename in nodenames:
        log.Info("Connecting to node {0}".format(nodename))
        node = nodesobj[nodename]
        try:
            node.createSession()
        except SessionCreateError as e:
            log.Error("Failed to connect to node {name}".format(name=node.getName()))
        except Exception as e:
            log.Error(e)

    log.Info("Successfully established connection with nodes")


def main():
    global loop
    global log
    global port	
    log	= Logger(Log.DEBUG)
    try:
        load_config()
    except (ConfigPathError,ConfigError) as e:
        log.Error("Error in Loading configuration {0} ".format(e))
        exit(255)
    except Exception as e:
        log.Error("Unknown Error in Loading configuration {0} ".format(e))
        exit(255)

    try:
        load_sessions()
    except (ConfigPathError,ConfigError,SessionCreateError) as e:
        log.Error("Error in connecting to nodes {0} ".format(e))
        exit(255)
    except Exception as e:
        log.Error("Unknown Error in  connecting to nodes {0} ".format(e))
        exit(255)
    register_signals()
    connection = Connection(port = int(port))
    connection.start_listener()

    while loop:
        try:
            connection.connection_handler()
        except Exception as e:
            log.Error(e)
            break
	
    connection.stop_listener()
    del connection

if __name__ == '__main__':
    main()
