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
			raise ConfigError
        config = Util.LoadConfiguration(config_path)
    except ConfigError as e:
		log.Error(e)
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


def load_module(modules, mod_name,config):
    try:
	print "loading "+mod_name
        mod = __import__(mod_name)
	script_obj = eval("mod."+mod_name)
        #print (modules[mod_name])

	ob = script_obj(config)  
        modules[mod_name] = ob	
	print mod_name+" loaded successfully"
    except ImportError as e:
    	print e
        print("Error in loading module " + mod_name)
        modules[mod_name] = None
    except AttributeError as e:
	print e	
        print("Error in loading module " + mod_name)
        modules[mod_name] = None
    except KeyError as e:
    	print e
        print("Error in loading module " + mod_name)
        modules[mod_name] = None
    except TypeError as e:
    	print e
        print("Error in loading module " + mod_name)
        modules[mod_name] = None

def load_modules(modules, config):
    try:
        module_path = Util.get_module_path(config)
	sys.path.append(module_path)
        for x in os.listdir(module_path):
            if ".py" == x[-3:]:
                mod_name = x[:-3]
                load_module(modules,mod_name,config)
    except Exception as e:
        raise e

def main():
    global loop
    global log 
    log	= Logger(Log.DEBUG)	
    ts = list()	
    modules = dict()
    config = load_config()
#sessions = initialize_sessions(config)

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
