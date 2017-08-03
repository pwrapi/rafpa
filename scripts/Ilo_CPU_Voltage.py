#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
from Log import Logger
from ExceptionCollection import ParamInResponseGetError
import json
log = Logger()

class Ilo_CPU_Voltage(generic):


    def get(self,session=None,entity=None,obj=None,attribute=None):
	 URL=Util.getURL(entity,obj,attribute,"get")
	 Param=Util.getParam(entity,obj,attribute,"get")
         value = generic.getValue(self,session,URL)
	 json_data = json.loads(value.text)
	
         try:
             AttrValue = json_data["Oem"]["Hp"][Param]
	 except Exception as e:
             log.Error("Error in finding Get Parameter in the Response")		   
	     raise ParamInResponseGetError

	 return AttrValue    
         
 

    
       
    
