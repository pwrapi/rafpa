#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util

#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_Chassis_Max_Power(generic):

    
    def __init__(self,configobj):
	generic.__init__(self,configobj)
        self.configobj = configobj
	#pass
    def get(self,entity=None,node=None,obj=None,attribute=None):
        try:
	   	
            URL = Util.getRedfishURL(self.configobj,"URL",entity,obj,attribute)
	    redfishValue = Util.getRedfishValue(self.configobj,"get",entity,obj,attribute)
	    Rest_OBJ = Util.get(self.configobj,node)
	    response = Rest_OBJ.rest_get(URL)
	    if redfishValue not in response.dict:
	       return 0
	    else:
	       Value = response.dict[redfishValue]
	          
            #Value = self.utilobj.get()
               print "Chassis Max Power:",Value
	       return Value
        except Exception as e:
#raise e
            return 1.0   

    
       
    
