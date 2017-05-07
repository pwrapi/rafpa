from Config import config as con
from Config import ConfigParser
from ExceptionCollection import HostNameMissing,UserNameMissing,PasswordMissing, \
	 							InvalidEntry,URIMissing,ParamMissing,ScriptMissing



class Devices(ConfigParser):
	def __init__(self, configfile, configpath=None):
		config = con(configfile,configpath)
		ConfigParser.__init__(self)
		for devicename in config:
			self[devicename] = device = Device(devicename,config[devicename])			

			

class Device(ConfigParser):

	def __init__(self,name,config):
		self.deviceName = name
		ConfigParser.__init__(self)
		
		for attr_name in config:
			try:
				self[attr_name] = attr = Attribute(attr_name)
				attr.setURL( config[attr_name]['URL'] )
				attr.setParam( config[attr_name]['get'] )
				attr.setScript(config[attr_name]['script'])

			except KeyError as e:
				if 'URL' in e:
					raise URIMissing
				elif 'get' in e:
					raise ParamMissing
				elif 'script' in e:
					raise ScriptMissing
				else:
					raise KeyError
			except TypeError as t:
					raise InvalidEntry


class Attribute(object):
	def __init__(self, attr_name):
		self.attr = attr_name
	
	def getName(self):
		return self.attr		
	
	def setURL(self, url):
		self.url = url
	
	def getURL(self):
		return self.url
	
	def setParam(self, param):
		self.param = param
	
	def getParam(self):
		return self.param
	
	def setScript(self, script_name):
		self.script = script_name
	
	def getScript(self):
		return self.script 
	
