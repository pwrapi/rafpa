#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
import re
from ExceptionCollection import ParamInResponseGetError
Proc_str=""
ProcDimm = ""
alist = []
from Log import Logger,Log
log = Logger(Log.DEBUG)
import string
import json

class Memory_Temperature(generic):

    def get(self,session=None,entity=None,obj=None,attribute=None):
        
	   dev = obj.replace("#","") 
	   dev = dev.split(".")
	   r = re.compile("([a-zA-Z]+)([0-9]+)")
	   d = dict([r.match(string).groups() for string in dev])

           Proc_Str = "P{0}".format(d["cpu"])   
           ProcDimm = Proc_Str + " DIMM"
   
	   URL=Util.getURL(entity,obj,attribute,"get")
	   Param=Util.getParam(entity,obj,attribute,"get")
	   value = generic.getValue(self,session,URL)
	   json_data = json.loads(value.text)
	   try:
	       for key in json_data['Temperatures']:
	           if ProcDimm in key['Name']:
	               alist.append(key['Name'])

	           for x in alist:

	               dimm = x
		       if Proc_str in dimm:
		           index = dimm.find('DIMM')
		           
		           dimm_range = dimm[index+5:]
	                   low,high= dimm_range.split("-")
	                   low = int(low)
                           high = int(high)

                           if low <= int(d["memory"]) <= high:
	                       if key['Name'] == x:
                                   return key[Param]
			           break        
                           				   
	                   else:
                               continue                  
			       
	   
           except Exception as e:
               log.Error("Error in finding Get Parameter in the Response")
	       raise ParamInResponseGetError
 

    
       
    
