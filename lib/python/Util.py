#this class has all the common functions required to interface with the other modules

import sys
from Config.RedfishReadConfig import config
from Session.Sessions import sessions



iloip = ""
username = ""
password = ""
nodelist = []
sessionsdict = {}
scriptnames = []
value = ""
scriptobjdict = {}
"""
def __init__(self,entity,object,attribute,action,iloname):

        self.entity = entity
        self.iloname = iloname
        self.object = object
        self.attribute = attribute
        self.action = action
    
def __init__(self):
        pass
"""    

def initialiseSession(configobj):
	global sessionsdict
        try:
            sessionsobj = sessions()
	    sessionsdict = getSession(sessionsobj,configobj)
            return sessionsobj
        except Exception as e:
            raise e

    
def getSession(sessionsobj,configobj):
	global sessionsdict
        try:
            
            nodelist = getNodeNames(configobj)
            for node in nodelist:
#print node
                iloip = getILoConfigurations(configobj,node,"iloIP")
		username = getILoConfigurations(configobj,node,"username")
		password = getILoConfigurations(configobj,node,"password")
#print iloip,username,password,node
                sessionsdict = sessionsobj.createSession(iloip,username,password,node)
#print sessionsdict
            return sessionsdict
                      
        except Exception as e:
            raise e


def initialiseConfiguration():
	global configobj
        try:
            configobj = config()
#print type(configobj)
            #configobj = config(self.entity,self.object,self.attribute,self.action,self.iloname)
            return configobj           
        except Exception as e:
            print "Could not initialise Configuration" , e


def getILoConfigurations(configobj,node,input):
        try:
            ilovalue = configobj.ReadILODetails(input,node)
#username = configobj.ReadILODetails("username",node)
#password = configobj.ReadILODetails("password",node)
#print iloip , username , password	
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
"""
def initializeAllScripts(self,utilobj,configobj):
        try:
        
            for script in self.scriptnames:
                print script
                s = "from scripts."+ script +" import "+ script
                s               
                scriptobj = +script+(utilobj,configobj)
                scriptobjdict[script] = scriptobj
            return scriptobjdict 
        except Exception as e:
            return e
"""

def get(configobj,node):
        try:
#getValue = getRedfishConfigurations(configobj,"get",entity,obj,attribute)
#getURL = getRedfishConfigurations(configobj,"URL",entity,obj,attribute)
            for key in sessionsdict:
                if key == node:
                    REST_OBJ = sessionsdict[key]
#response = REST_OBJ.rest_get(getURL)
#if getValue not in response.dict:
#"No Value found"
#else:
#return str(response.dict[getValue])
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
           	   
