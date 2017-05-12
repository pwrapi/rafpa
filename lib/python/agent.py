from Connection import Connection
import signal
import Util
import os
import sys
from Log import Logger,Log  
from ExceptionCollection import ConfigError



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

    try:
        config_path = os.environ.get('CONFIG_PATH')
        if config_path == None:
            log.Error("CONFIG_PATH is not set")
            raise ConfigError
        dconfig = Util.LoadConfiguration(config_path)
    except ConfigError as e:
        log.Error("Error in Loading configuration {0} ".format(e))
        exit(255)
    else:
        log.Info("Successfully Loaded Configuration database")
		
	
def load_sessions():
    try:
        config_path = os.environ.get('CONFIG_PATH')
        if config_path == None:
            raise ConfigError
        Util.LoadSessionConfig(config_path)

    except ConfigError as e:
        log.Error(e)
        exit(255)
    else:
        pass

def main():
    global loop
    global log 
    log	= Logger(Log.DEBUG)
    load_config()
    load_sessions()

#   load_modules(modules,config)
'''	
    register_signals() 	
    connection = Connection()
    connection.start_listener()

    while loop:
	connection.connection_handler(config, sessions, modules,ts)
connection.stop_listener()
connection.cleanup()
'''
if __name__ == '__main__':
    main()
