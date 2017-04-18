#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util

#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_CPU_Freq(object):

    
    def __init__(self,configobj):
	#generic.__init__(self,utilobj,configobj)
        self.configobj = configobj
	#pass
    def get(self,entity,node,obj,attribute):
        try:
	   	
            Value = Util.get(self.configobj,entity,obj,attribute,node)
            #Value = self.utilobj.get()
            #print "Chassis Max Power:",Value
	    return Value
        except Exception as e:
            raise e
 

    
       
    
