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
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
# THEORY OF LIABILITY,WHETHER IN CONTRACT,STRICT LIABILITY,OR TORT(INCLUDING 
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import os
from ExceptionCollection import SessionCreateError,deviceConfigReadError, \
    ConfigPathError,ModuleImportError,AgentRootPathError,ScriptsPathError,SessionGetError,AttrGetError,URLGetError,ParamGetError,DynamicURLCreateError,GetConnectionError
from Config import config
from Devices import Devices
from Nodes import Nodes
from Log import Logger
import string

log = Logger()

configobj = dict()
nodesobj = dict()

try:
    from ilorestobject import RestObject
except ImportError:
    log.Warn("For In-Band Communication, Install python-ilorest-library")
import sushy


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
    suffix = conffile[-4:]
    if suffix == "yaml":
        # It is a YAML file
        return True
    return False

def getConfigObj():
    global configobj
    return configobj

def getNodesobj():
    global nodesobj
    return nodesobj


def getNodeNames():
    return getNodesobj().keys()

def redfish_server_login(host, username, password):
    return createSession(host,username,password)

def createSession(host,username,password):
    REST_OBJ = getRestObject(host,username,password)
    return REST_OBJ

def sushy_server_login(host,username,password):
    return createSushySession(host,username,password)

def createSushySession(host,username,password):
    SUSHY_OBJ = getSushyObject(host,username,password)
    return SUSHY_OBJ	

def getRestObject(host,username,password):
    Account,Password = None,None
    if host == "localhost" :
        https_url = "blobstore://."
        Account = "None"
        Password = "None"
    else:
        https_url = "https://"+ host
        Account = username
        Password = password

    restobj = RestObject(https_url,Account,Password)
    return restobj
def getSushyObject(host,username,password):
    Account,Password = None,None
    if username == "None" :	
        https_url = "http://"+ host
    else:
        https_url = "https://"+ host
    Account = username
    Password = password
    		
    try:
       sushyobj = sushy.Sushy(https_url+"/redfish/v1",Account,Password,verify = False)
    except Exception as e:
       raise GetConnectionError
    else:    	
       sushyconnobj = sushy.connector.Connector(https_url,Account,Password,verify = False)
       return sushyconnobj	
    	

def load_module(mod_name, device, attribute):
    try:
        log.Info("Importing module {0}".format(mod_name))
        mod = __import__(mod_name)
        log.Debug("Module {0}  imported ".format(mod_name))
        Object_hash = eval("mod."+mod_name)
        Object = Object_hash(device, attribute)
        log.Info(mod_name+" loaded successfully")
    except (ImportError, AttributeError,KeyError,TypeError) as e:
        log.Error("Loading module {module} was unsuccesssful {exc}".format(module=mod_name,exc=e))
        raise ModuleImportError
    except Exception as e:
        log.Error("Loading module {module} was unsuccesssful {exc}".format(module=mod_name, exc=e))
        raise ModuleImportError
    else:
        return Object

def get_config_path():

    config_path = os.path.join(get_redfish_agent_root_path(), "config")
    if config_path == None or os.path.isdir(config_path) == False:
        log.Error("config directory not.")
        raise ConfigPathError
    else:
        return config_path

def get_scripts_path():

    config_path = os.path.join(get_redfish_agent_root_path(), "scripts")
    if config_path == None or os.path.isdir(config_path) == False:
        log.Error("scripts directory not found.")
        raise ScriptsPathError
    else:
        return config_path

def get_redfish_agent_root_path():
    agent_path = os.environ.get('REDFISH_AGENT_ROOT')
    if agent_path == None or os.path.isdir(agent_path) == False:
        log.Error("Environment varaible REDFISH_AGENT_ROOT is not set.")
        raise AgentRootPathError
    else:
        return agent_path


def gethandler(entity, device, attr):
    try:
        return getConfigObj()[entity][device][attr].getmodobj()
    except KeyError as e:
        log.Error("Error getting attribute from {0} {1} {2}".format(entity,device,attr))
        raise AttrGetError
def getNode(host):
    try:
        return nodesobj[host]
    except KeyError as e:
        log.Error("Error getting node information for host {hostname}".format(hostname=host))
        raise SessionGetError

def getURL(entity,device,attr,op):
    try:
        query_device = device.rsplit(".")[-1]
        query_device = query_device.split('#')[0]
        if (op == "get"):
            dynURL = getConfigObj()[entity][query_device][attr].getGetURL() 
        else:
            dynURL = getConfigObj()[entity][query_device][attr].getSetURL()

        return createDynamicURL(device,dynURL)
	
    except KeyError as e:
        log.Error("Error getting URL from {0} {1} {2}".format(entity,device,attr))
        raise URLGetError

def getParam(entity,device,attr,op):
    try:
        query_device = device.rsplit(".")[-1]
        query_device = query_device.split('#')[0]
        if (op == "get"):	 	
            return getConfigObj()[entity][query_device][attr].getGetParam()
        else:
            return getConfigObj()[entity][query_device][attr].getSetParam()				
    except KeyError as e:
        log.Error("Error getting Param from {0} {1} {2}".format(entity,device,attr))
        raise ParamGetError
def createDynamicURL(device,URL):
    try:
        devices = device.split(".")
        newlist=[]
        for devs in devices:
            newlist.append(devs.split("#"))
        devDic = dict(newlist)
        newURL=''
        for key in devDic:
            if key in URL:
                replacestring = "{" + key + "}"
                newURL = string.replace(URL,replacestring,devDic[key])
                URL = newURL
	return URL
    except KeyError as e:
        log.Error("Error creating dynamic URL from {0} {1}".format(device,URL))
        raise DynamicURLCreateError	
