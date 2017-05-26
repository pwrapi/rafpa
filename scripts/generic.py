import sys
import os
import Util
import ExceptionCollection
from Log import Logger,Log
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
            return -1
        return value	    
	    

	
 

    
       
    
