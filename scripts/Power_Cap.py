#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
from Log import Logger
#from Log import Log
from ExceptionCollection import ParamInResponseGetError,ResponseSetError
import json
#log = Logger(Level=Log.DEBUG)
log = Logger()

class Power_Cap(generic):


    def get(self,session=None,entity=None,obj=None,attribute=None):
	 URL=Util.getURL(entity,obj,attribute,"get")
	 Param=Util.getParam(entity,obj,attribute,"get")
         value = generic.getValue(self,session,URL)
	 json_data = json.loads(value.text)
	
         try:
             AttrValue = json_data["PowerLimit"][Param]
	 except Exception as e:
             log.Error("Error in finding Get Parameter in the Response")		   
	     raise ParamInResponseGetError

	 return AttrValue
    
    def set(self,session=None,entity=None,obj=None,attribute=None,value=None):
        URL=Util.getURL(entity,obj,attribute,"set")
        Param=Util.getParam(entity,obj,attribute,"set")
        data={ "PowerControl": [ {"PowerLimit": {Param: int(value) }} ] }		
        value = generic.setValue(self,session,URL,data)
        StatusCode = value.status_code
         	
        return StatusCode

         
     
     
    
       
    
