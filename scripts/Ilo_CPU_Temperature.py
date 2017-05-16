#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
import re
CPUName=""

#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_CPU_Temperature(generic):


    def get(self,entity,node,obj,attribute):
        try:
#obj="CPU1"
	   CPUNum = obj.split("CPU",1)[1]
           CPUName = "CPU " + CPUNum
	   URL = Util.getRedfishURL(self.configobj,"URL",entity,"CPU",attribute)
	       
           redfishValue = Util.getRedfishValue(self.configobj,"get",entity,"CPU",attribute)
           Rest_OBJ = Util.get(self.configobj,node)
           response = Rest_OBJ.rest_get(URL)
	   for key in response.dict['Temperatures']:
	       if CPUName in key['Name']:
                    print (key[redfishValue])
	            break
	       else:
                    continue                  
	            return -1
	       
        except Exception as e:
            raise e
 

    
       
    
