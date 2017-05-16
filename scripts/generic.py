import sys
import os
import Util
import ExceptionCollection
from Log import Logger,Log

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


	

	
 

    
       
    
