#this class has all the common functions required to interface with the other modules

import sys
import os
from ExceptionCollection import SessionCreateError,deviceConfigReadError, \
    ConfigPathError,ModuleImportError,AgentRootPathError,ScriptsPathError,SessionGetError,AttrGetError
from Config import config
from Devices import Devices
from Nodes import Nodes
from Log import Logger

log = Logger()

configobj = dict()
nodesobj = dict()


from _restobject import RestObject


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

    restobj = RestObject(https_url, Account, Password)
    return restobj

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
def getsession(host):
    try:
        return nodesobj[host]
    except KeyError as e:
        log.Error("Error getting node information for host {hostname}".format(hostname=host))
        raise SessionGetError

