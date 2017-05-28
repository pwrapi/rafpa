#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
import re
from ExceptionCollection import ParamInResponseGetError
CPUName=""
import json
from Log import Logger
log = Logger()

#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_CPU_Temperature(generic):


    def get(self,session=None,entity=None,obj=None,attribute=None):
        
#obj="CPU1"
#CPUNum = obj.split("CPU",1)[1]
#CPUName = "CPU " + CPUNum
	   
	   devices = obj.split(".")
	   newlist=[]
	   for devs in devices:
	       newlist.append(devs.split("#"))
	   devDic = dict(newlist)
           CPUNum = devDic["cpu"]
           CPUName = "CPU " + CPUNum 	       
	   
	    
	   URL=Util.getURL(entity,obj,attribute)
	   Param=Util.getParam(entity,obj,attribute)

	   value = generic.getValue(self,session,URL)
	   json_data = json.loads(value.text)
           try:

	       for key in json_data['Temperatures']:
	           if CPUName in key['Name']:
                        return key[Param]
	                break

	           else:
                        continue                  
	                
	           
           except Exception as e:
               log.Error("Error in finding Get Parameter in the Response")
	       raise ParamInResponseGetError
	      
 

    
       
    
