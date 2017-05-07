#this class has all the common functions required to interface with the other modules

import sys
import os
from ExceptionCollection import SessionCreateError,deviceConfigReadError,ConfigPathError
from progress.bar import ShadyBar as Bar
from Config import config
from Devices import Devices
from Nodes import Nodes
from _restobject import RestObject
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
			nodes = Nodes(conffile,nodes_dir)
			nodesobj.update(nodes)



def isyaml(conffile):
	prefix,sep,suffix = conffile.partition(".")
	if suffix == "yaml":

		# It is a YAML file 
		return True
	return False

def getSessionobj():
	return sessionsdict
			

def getNodeNames(configobj):
	pass
          
           	   
def redfish_server_login(host, username, password):
	return createSession(host,username,password)

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
               
