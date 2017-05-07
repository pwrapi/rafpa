from Config import config as con
from Config import ConfigParser
from time import time
from ExceptionCollection import HostNameMissing,UserNameMissing,PasswordMissing,InvalidEntry



class Nodes(ConfigParser):
	def __init__(self, configfile, configpath=None):
		config = con(configfile,configpath)
		ConfigParser.__init__(self)
		for nodename in config:
			self[nodename] = node = Node(nodename)
			try:
				node.setHost(config[nodename]['hostname'])	
				node.setUsername(config[nodename]['username'])	
				node.setPassword(config[nodename]['password'])	
			except KeyError as ke:
				if 'hostname' in ke:
					raise HostNameMissing
				elif 'username' in ke:
					raise UserNameMissing
				elif 'password' in ke:
					raise PasswordMissing
				else:
					raise KeyError
			except TypeError as t:
				raise InvalidEntry
			


class Node(object):

	def __init__(self,name):
		self.name = name
		self.active = False
		self.session = None
	def getName(self):
		return self.name
	def setHost(self, hostname):
		self.hostname = hostname
	def getHost(self):
		return self.hostname
	def setUsername(self, username):
		self.username = username
	def getUsername(self):
		return self.username
	def setPassword(self, password):
		self.password = password
	def getPassword(self):
	    return self.password
	
	def createSession():
		retries = 1	
		while retries < 3:	
			try:
				log("Connectiing to server {host} with {user} try {tries}".format(host=self.hostname, user=self.username,tries=retries)	
				session = Util.redfish_server_handshake(self.hostname,self.username,self.password)
			except RedfishServerNotExists as e:
				self.active(False)
				raise SessionCreateError
			except RedfishServerCredentialError as e:
		 		raise SessionCreateError
			except Exception as e:
				log(e)
				retries += 1
			else:
				self.storeSessionInfo(session)
				self.setActive(True)

			

	def storeSessionInfo(self, session, time=time()):
		S = Session(session,time)
		self.session = s
		self.expired = False
			
		
	def getSession(self):
		return self.session.getSession()

	def isActive(self):
		return self.active
	def setActive(self, state):	
		self.active = state

class Session():
	def __init__(self):
		self.session = None
		self.expired= True
	def load(self,session, time= time()):	
		self.session = session
		self.start = time
		self.elapsed = 0
		self.expired = False		
	def __del__(self):
		# Log out of the session
		# Mark Session as expired
		pass

	def get():
		if self.expired:
			raise SessionExpired
		else:
			return self.session
