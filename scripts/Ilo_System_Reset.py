#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
from Log import Logger
from ExceptionCollection import ResponseSetError
import json
log = Logger()
#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_System_Reset(generic):

    
    def set(self,session=None,entity=None,obj=None,attribute=None,value=None):
	 URL=Util.getURL(entity,obj,attribute)
	 Param=Util.getParam(entity,obj,attribute)
	 data={Param:value}
         Action = URL + "Actions/Oem/Hp/ComputerSystemExt.SystemReset/"	 
         value = generic.postValue(self,session,Action,data)
         StatusCode = value.status_code
                  	
	 return StatusCode

         
     
     
    
       
    
