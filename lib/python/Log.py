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

