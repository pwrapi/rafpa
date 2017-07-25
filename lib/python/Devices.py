from Config import config as con
from Config import ConfigParser
from ExceptionCollection import HostNameMissing,UserNameMissing,PasswordMissing, \
                                InvalidEntry,URIMissing,ParamMissing,ScriptMissing, \
                                ModuleImportError

from Log import Logger

log = Logger()

class Devices(ConfigParser):
    def __init__(self, configfile, configpath=None):
        config = con(configfile,configpath)
        ConfigParser.__init__(self)

        for devicename in config:
            self[devicename] = device = Device(devicename,config[devicename])
            
import Util
class Device(ConfigParser):

    def __init__(self,name,config):
        self.deviceName = name
        ConfigParser.__init__(self)
        for attr_name in config:
            self[attr_name] = attr = Attribute(attr_name)				
            try:    
                attr.setGetURL( config[attr_name]['get']['URL'] )
                attr.setGetParam( config[attr_name]['get']['attribute'] )
                attr.setGetScript(config[attr_name]['get']['script'])
            except KeyError as e:
                			
                attr.setGetURL("NA")
                attr.setGetParam("NA")
                attr.setGetScript("NA")
            try:	
                attr.setSetURL( config[attr_name]['set']['URL'] )
                attr.setSetParam( config[attr_name]['set']['attribute'] )
                attr.setSetScript(config[attr_name]['set']['script'])

            except KeyError as e:
                
                attr.setSetURL("NA")
                attr.setSetParam("NA")
                attr.setSetScript("NA")
            except TypeError as t:
                raise InvalidEntry

    def getName(self):
        return self.deviceName

class Attribute(object):
    def __init__(self, attr_name):
        self.attr = attr_name
        self.mod_obj = None
        self.valid = False
    def getName(self):
        return self.attr        
    
    def setGetURL(self, geturl):
        self.geturl = geturl
    
    def getGetURL(self):
        return self.geturl
    
    def setGetParam(self, getparam):
        self.getparam = getparam
    
    def getGetParam(self):
        return self.getparam
    
    def setGetScript(self, getscript_name):
        self.getscript = getscript_name
    
    def getGetScript(self):
        return self.getscript

    def setSetURL(self, seturl):
        self.seturl = seturl
    
    def getSetURL(self):
        return self.seturl
    
    def setSetParam(self, setparam):
        self.setparam = setparam
    
    def getSetParam(self):
        return self.setparam
    
    def setSetScript(self, setscript_name):
        self.setscript = setscript_name
    
    def getSetScript(self):
        return self.setscript
    def setValid(self, boolean):
        self.valid = boolean

    def load(self,device):
        mod_name = self.getGetScript().partition(".")[0]
        if (mod_name == "NA"):
           mod_name = self.getSetScript().partition(".")[0]		
        try:
          if (mod_name <> "NA"):
            mod_obj = Util.load_module(mod_name,device, self)
            self.mod_obj = mod_obj
            self.setValid(True)
        except ModuleImportError as e:
            log.Error("Loading module \"{modname}\" for device \"{dev}\" and attribute \"{attr}\" was \
unsuccessful".format(modname=mod_name, dev=device.getName(),attr=self.getName()))

            self.setValid(False)
    def getmodobj(self):
        return self.mod_obj
