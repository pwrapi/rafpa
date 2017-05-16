#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
import re
Proc_str=""
ProcDimm = ""
alist = []
#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_Memory_Temperature(generic):

    def get(self,entity=None,node=None,obj=None,attribute=None):
        try:
#obj="proc1.dimm8"
	   obj = obj.split(".")
	   r = re.compile("([a-zA-Z]+)([0-9]+)")
	   d = dict([r.match(string).groups() for string in obj])

           Proc_Str = "P{0}".format(d["proc"])   
           ProcDimm = Proc_Str + " DIMM"
   
	   URL = Util.getRedfishURL(self.configobj,"URL",entity,"Memory",attribute)
	       
           redfishValue = Util.getRedfishValue(self.configobj,"get",entity,"Memory",attribute)
           Rest_OBJ = Util.get(self.configobj,node)
           response = Rest_OBJ.rest_get(URL)
	   for key in response.dict['Temperatures']:
	       if ProcDimm in key['Name']:
	           alist.append(key['Name'])

	       for x in alist:

	           dimm = x
		   if Proc_str in dimm:
		       index = dimm.find('DIMM')
		       if index < 0:
		           return -1
		       dimm_range = dimm[index+5:]
	               low,high= dimm_range.split("-")
	               low = int(low)
                       high = int(high)

                       if low <= int(d["dimm"]) <= high:
	                   if key['Name'] == x:
                               print (key[redfishValue])
			       break
	               else:
                           continue                  
			   return -1
	   
        except Exception as e:
            raise e
 

    
       
    
