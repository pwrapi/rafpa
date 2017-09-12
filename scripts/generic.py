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
import Util
import ExceptionCollection
from Log import Logger,Log
from ExceptionCollection import ValueGetError,ValueSetError
import json

log = Logger()

class generic(object):

    def __init__(self,device,attribute):
        self.device = device
        self.attribute = attribute
        log.Debug("Called init in generic module for {0} {1}".format(device.getName(), attribute.getName()))
    def getDevice(self):
        return self.device
    def getAttribute(self):
        return self.attribute
    def getValue(self,session,URL):
        try:
            value = session.get(URL)
	except Exception as e:
	    log.Error("Error getting value for the session object")
            raise ValueGetError
        return value
    
    def setValue(self,session,URL,data):
        try:
            value = session.patch(URL,data)
	except Exception as e:
	    log.Error("Error setting value for the session object")
            raise ValueSetError
        return value
		 
    def postValue(self,session,URL,data):
        try:
            value = session.post(URL,data)
	except Exception as e:
	    log.Error("Error setting value for the session object")
            raise ValueSetError
        return value

    
       
    
