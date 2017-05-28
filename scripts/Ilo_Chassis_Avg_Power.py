#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
from Log import Logger
from ExceptionCollection import ParamInResponseGetError
import json
log = Logger()
#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_Chassis_Avg_Power(generic):


    def get(self,session=None,entity=None,obj=None,attribute=None):
	 URL=Util.getURL(entity,obj,attribute)
	 Param=Util.getParam(entity,obj,attribute)
         value = generic.getValue(self,session,URL)
	 json_data = json.loads(value.text)
	
         try:
             AttrValue = json_data[Param]
	 except Exception as e:
             log.Error("Error in finding Get Parameter in the Response")		   
	     raise ParamInResponseGetError

	 return AttrValue    
         
 

    
       
    
