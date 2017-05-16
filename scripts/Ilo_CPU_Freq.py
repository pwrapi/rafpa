#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util

#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_CPU_Freq(generic):

    

    def get(self,entity=None,node=None,obj=None,attribute=None):
        try:
	    URL = Util.getRedfishURL(self.configobj,"URL",entity,obj,attribute)
            redfishValue = Util.getRedfishValue(self.configobj,"get",entity,obj,attribute)
            Rest_OBJ = Util.get(self.configobj,node)
	    print Rest_OBJ
            response = Rest_OBJ.rest_get(URL)
            if redfishValue not in response.dict:
               return 0
            else:
	       Value = response.dict[redfishValue]
               
               print "CPU Freq:",Value
	       return Value
        except Exception as e:
#raise e    
	    return 1.0
 

    
       
    
