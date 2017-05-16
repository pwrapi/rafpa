#this function is written to get or set value chassis avg power

import sys
import os
from generic import generic
import Util
from Log import Logger

log = Logger()
#sys.path.append("/root/home/vinanti/redfishagent")

class Ilo_Chassis_Avg_Power(generic):


    def get(self,entity=None,node=None,obj=None,attribute=None):
	    return 1.0
 

    
       
    
