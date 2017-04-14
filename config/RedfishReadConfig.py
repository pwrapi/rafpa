#This code is to read the configuration for all the objects and attributes
#!/usr/bin/env python


import sys
import yaml
#import SessionManager

class config(object):
    
    """
    def __init__(self,entity,obj,attribute,action,iloname):
        
        self.entity = entity
        self.obj = obj
        self.attribute = attribute
        self.action = action
        self.iloname = iloname
    """
    def __init__(self):
        pass
    
    def get_config_data(self,input,entity,obj,attribute):
        try:
       #strSourceFileName = strFileName
            stream =  file("Redfish.yaml", 'r')
            yamlConfigData = yaml.safe_load(stream)
            stream.close()
            valuefromconfig = yamlConfigData[entity][obj][attribute][input]           
            return valuefromconfig
        except Exception as e:
            print "Error Getting Configuration Data , Error in :" , e

    def ReadILODetails(self,input,iloname):
        try:
            stream = file("iloConfig.yaml",'r')
            yamlConfigData = yaml.safe_load(stream)
            stream.close()
            IloValue = yamlConfigData[iloname][input]
            return IloValue
        except Exception as e:
            print "Error Getting Configuration Data , Error in :" , e

    def ReadNode(self):
        try:
            stream = file("iloConfig.yaml",'r')
            yamlConfigData = yaml.safe_load(stream)
            stream.close()
            nodeValue = yamlConfigData["nodename"]
            return nodeValue
        except Exception as e:
            print "Error Getting Configuration Data , Error in :" , e
    
    def ReadGlobalConfig(self,data):
         try:
            stream = file("Redfish.yaml",'r')
            yamlConfigData = yaml.safe_load(stream)
            stream.close()
            output = yamlConfigData["config"][data]
            return output
         except Exception as e:
            print "Error Getting Configuration Data , Error in :" , e
    

      
           



