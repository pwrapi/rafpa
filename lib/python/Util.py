#this class has all the common functions required to interface with the other modules

import sys
import os
from ExceptionCollection import SessionCreateError,deviceConfigReadError,ConfigPathError
from progress.bar import ShadyBar as Bar
from Config import config
from Devices import Devices
from Nodes import Nodes

from Session.Sessions import sessions

configobj = dict()
nodesobj = dict()
sessionsdict = dict()

def LoadConfiguration(configdir):
	readDeviceConfigDir(configdir)

def LoadSessions(configdir):
	readNodeConfigDir(configdir)	

def readDeviceConfigDir(configdir,device_dir="devices"):
	global configobj
	device_dir = os.path.join(configdir,device_dir)
	conf_files = list()
		
	try:
		conf_files = os.listdir(device_dir)
	except OSError as e:
		raise ConfigPathError
    
	for conffile in conf_files:
		full_path = os.path.join(device_dir,conffile)
		if os.path.isfile(full_path) and isyaml(full_path):
			entity = conffile.partition(".")[0]
			configobj[entity] = Devices(conffile,device_dir)
	
def readNodeConfigDir(configdir,nodes_dir="location"):
	global nodesobj
	nodes_dir = os.path.join(configdir,nodes_dir)
	conf_files = list()
		
	try:
		conf_files = os.listdir(nodes_dir)
	except OSError as e:
		raise ConfigPathError

	for conffile in conf_files:
		full_path = os.path.join(nodes_dir,conffile)
		if os.path.isfile(full_path) and isyaml(full_path):
			nodesionobj = Nodes(conffile,nodes_dir)
			nodesobj.update(nodes)


def getSessionobj():
	return sessionsdict

def CreateSessions():
	
	sessions = getSessionobj()	
	for node in sessions:
		nodeobj = sessions[node]

		host = nodeobj.getHost()
		user = nodeobj.getUsername()
		password = nodeobj.getPassword()
		s = create_session(host, user, password)
		nodesobj.storeSessionInfo(s)



def isyaml(conffile):
	prefix,sep,suffix = conffile.partition(".")
	if suffix == "yaml":

		# It is a YAML file 
		return True
	return False

			

def getILoConfigurations(configobj,node,input):
        try:
            ilovalue = configobj.ReadILODetails(input,node)
            return ilovalue   
        except Exception as e:
            raise e


def getRedfishConfigurations(configobj,input,entity,obj,attribute):
        try:
            value = configobj.get_config_data(input,entity,obj,attribute)
            return value
        except Exception as e:
            raise e


def getNodeNames(configobj):
	
        try:
            nodenames = configobj.ReadNode()
            nodelist = nodenames.split(",")
            #print self.nodelist
            return nodelist
        except Exception as e:
            raise e

          
def getallScripts(configobj):
        try:
            names = configobj.ReadGlobalConfig("scriptnames")
            scriptnames = names.split(",")
            return scriptnames
        except Exception as e:
            raise e


def get(configobj,node):
        try:
            for key in sessionsdict:
                if key == node:
                    REST_OBJ = sessionsdict[key]
                    return REST_OBJ
            
        except Exception as e:
            raise e


def set(self):
        try:
            print("test")
        except Exception as e:
            raise e

        
def gethandler(configobj,entity,obj,attribute):
	try:
	    
	    getHandler = getRedfishConfigurations(configobj,"script",entity,obj,attribute)
	    
	    return getHandler
	except Exception as e:
	    raise e

def getRedfishValue(configobj,input,entity,obj,attribute):
        try:
	   getValue = getRedfishConfigurations(configobj,input,entity,obj,attribute)
	   return getValue
	except Exception as e:
           raise e

def getRedfishURL(configobj,input,entity,obj,attribute):
        try:
	   getURL = getRedfishConfigurations(configobj,input,entity,obj,attribute)
	   return getURL
        except Exception as e:
           raise e

def get_module_path(configobj):
        try:
           getPath = configobj.ReadGlobalConfig("location")
           return getPath
        except Exception as e:
           raise e
           	   
def redfish_server_login(host, username, password):
	return createsession(host,username,password)

def createSession(host,username,password):
	REST_OBJ = getRestObject(host,username,password)
	return REST_OBJ
            
            
def getRestObject(host,username,password):
	if host == "localhost" :
		https_url = "blobstore://."
		account = "None"
		password = "None"
	else:
		https_url = "https://"+ host
 		account = username
		password = password

	restobj = RestObject(https_url, account, password)
	return restobj
               
