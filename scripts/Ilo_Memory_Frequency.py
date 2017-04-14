#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import UtilBack

#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_Memory_Frequency(object):


    
    def __init__(self,configobj):
	#generic.__init__(self,utilobj,configobj)
        self.configobj = configobj
	#pass
    def get(self,entity=None,node=None,obj=None,attribute=None):
        try:
#print obj
#obj = 'proc:1.dimm:8'
	   b =':.'
	   for char in b:
	       obj = obj.replace(char,"")

	   URL = UtilBack.getRedfishURL(self.configobj,"URL",entity,"Memory",attribute)
	   URL = URL + obj
           redfishValue = UtilBack.getRedfishValue(self.configobj,"get",entity,"Memory",attribute)
           Rest_OBJ = UtilBack.get(self.configobj,node)
           response = Rest_OBJ.rest_get(URL)
           if redfishValue not in response.dict:
               return 0
           else:
               print str(response.dict[redfishValue])

#Value = Util.get(self.configobj,entity,obj,attribute,node)
            #Value = self.utilobj.get()
#print "Chassis Avg Power:",Value
        except Exception as e:
            raise e
 

    
       
    
