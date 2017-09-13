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
import logging
import syslog
from ExceptionCollection import InvalidLogLevel


class Log(object):
    
    DEBUG =logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    INFO = logging.INFO
    SYSLOG_IDENT = "Redfish Agent"


    syslog_level = { DEBUG : syslog.LOG_DEBUG,
    		      WARNING : syslog.LOG_WARNING,
	  	      ERROR : syslog.LOG_ERR,
	              INFO : syslog.LOG_INFO,
	           }	      

    def __init__(self, level=WARNING):
        self.logger = logging.getLogger()
	formatter = logging.Formatter("%(name)s %(levelname)s %(asctime)s %(message)s") 
        console = logging.StreamHandler(stream=sys.stderr)
	console.setFormatter(formatter)
        self.logger.addHandler(console)
	syslog.openlog(ident= Log.SYSLOG_IDENT, logoption=syslog.LOG_PID)
        self.level = level
	self.syslog_level = Log.syslog_level[level]
        self.logger.setLevel(self.level)
	syslog.setlogmask(syslog.LOG_UPTO(syslog.LOG_WARNING))

    def setLevel(self,level):
	if level !=  Log.DEBUG and \
		 level != Log.WARNING and \
     		 level != Log.ERROR and  \
		 level != Log.INFO : 
            raise IncorrectLogLevel
        else:
	   self.level = level
	   self.syslog_level = Log.syslog_level[level]	
           self.logger.setLevel(self.level)
	   syslog.setlogmask(syslog.LOG_UPTO(self.syslog_level))
	    	

    def Debug(self, message):
        self.logger.debug(message)
	syslog.syslog(syslog.LOG_DEBUG, message)
    def Warn(self, message):
        self.logger.warning(message)
	syslog.syslog(syslog.LOG_WARNING, message)
    def Error(self, message):
        self.logger.error(str(message))
	syslog.syslog(syslog.LOG_ERR, str(message))
    def Info(self, message):
        self.logger.info(message)
	syslog.syslog(syslog.LOG_INFO, message)

obj =  Log()
def Logger(Level=None):
	if Level != None :
		obj.setLevel(Level)
	return obj

