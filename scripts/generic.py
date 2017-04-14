#this function is written to get or set value chassis avg power

import sys
import os
import Util
#from config.Util import Util

#sys.path.append("/root/home/vinanti/redfishagent")

class generic(object):

    
    def __init__(self,utilobj,configobj):
	
#self.utilobj = utilobj
        self.configobj = configobj
	print "I am generic"
    def get(self):
	Value = 0    
        try:
	   	
            Value = self.utilobj.get(self.configobj)
            print value
        except Exception as e:
            raise e
        queue.put(Value)
	return Value


	
 

    
       
    
