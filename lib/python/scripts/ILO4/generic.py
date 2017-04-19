#this function is written to get or set value chassis avg power

import sys
import os
import Util
#from config.Util import Util

#sys.path.append("/root/home/vinanti/redfishagent")

class generic(object):

    
    def __init__(self,configobj):
	
#self.utilobj = utilobj
        self.configobj = configobj
	print "I am generic"
    def run(self,queue,entity,host,device_name,attr):
	Value = 0    
        try:
	   	
            Value = self.get(entity,host,device_name,attr)
            print value
        except Exception as e:
            raise e
        queue.put(Value)
	return Value


	
 

    
       
    
