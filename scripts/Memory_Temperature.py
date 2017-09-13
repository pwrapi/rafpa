# Copyright 2017 Hewlett Packard Enterprise Development LP
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may
# be used to endorse or promote products derived from this software without specific
# prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,WHETHER IN
# CONTRACT,STRICT LIABILITY,OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
# WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


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
 

    
       
    
