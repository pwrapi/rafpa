from Connection import Connection
import signal
import Util
import os
import sys
from Log import Logger,Log  
from ExceptionCollection import ConfigError, ConfigPathError, SessionCreateError



log = None

loop = 1
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
    dconfig = Util.LoadConfiguration(config_path)
    log.Info("Successfully Loaded Configuration database")

def load_sessions():

    config_path = Util.get_config_path()
    Util.LoadSessions(config_path)
    nodenames = Util.getNodeNames()
    for node in iter(Util.getNodesobj().values()):
        try:
            #node.createSession()
            pass
        except SessionCreateError as e:
            log.Error("Failed to connect to node {name}".format(node.getName()))

    log.Info("Successfully established connection with nodes")


def main():
    global loop
    global log 
    log	= Logger(Log.DEBUG)
    try:
        load_config()
    except (ConfigPathError,ConfigError) as e:
        log.Error("Error in Loading configuration {0} ".format(e))
        exit(255)
    except Exception as e:
        log.Error("Unknown Error in Loading configuration {0} ".format(e))
    try:
        load_sessions()
    except (ConfigPathError,ConfigError) as e:
        log.Error("Error in connecting to nodes {0} ".format(e))
        exit(255)
    except Exception as e:
        log.Error("Unknown Error in  connecting to nodes {0} ".format(e))
    register_signals() 	
    connection = Connection()
    connection.start_listener()

    while loop:
        try:
            connection.connection_handler()
        except Exception as e:
            log.Error(e)
            break
	
    connection.stop_listener()
    connection.cleanup()

if __name__ == '__main__':
    main()
