#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
from Log import Logger
import json
log = Logger()
#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_Chassis_Avg_Power(generic):


    def get(self,session=None,entity=None,obj=None,attribute=None):
	 URL=Util.getURL(entity,obj,attribute)
	 print URL
         Param=Util.getParam(entity,obj,attribute)
         print Param	
	 value1 = session.get(URL)
	 json_data1 = json.loads(value1.text)
         
	 if Param not in json_data1:
	     return 1.0
	 else:
	     b = json_data1[Param]
             return b

 

    
       
    
