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
from Log import Logger
#from Log import Log
from ExceptionCollection import ParamInResponseGetError,ResponseSetError
import json
#log = Logger(Level=Log.DEBUG)
log = Logger()

class System_PState(generic):


    def get(self,session=None,entity=None,obj=None,attribute=None):
	 URL=Util.getURL(entity,obj,attribute,"get")
	 Param=Util.getParam(entity,obj,attribute,"get")
         value = generic.getValue(self,session,URL)
	 json_data = json.loads(value.text)
	
         try:
             AttrValue = json_data["Oem"]["Hp"][Param]
	 except Exception as e:
             log.Error("Error in finding Get Parameter in the Response")		   
	     raise ParamInResponseGetError

	 return AttrValue
    
    def set(self,session=None,entity=None,obj=None,attribute=None,value=None):
        URL=Util.getURL(entity,obj,attribute,"set")
        Param=Util.getParam(entity,obj,attribute,"set")
        try:

            if (value == "Max" or value == "Min"):
            
                data={ "Oem": {"Hp": {Param: value }} }
                value = generic.setValue(self,session,URL,data)
                StatusCode = value.status_code
            else:
                raise Exception
        except Exception as e:
            raise ResponseSetError	
         	
        return StatusCode

         
     
     
    
       
    
