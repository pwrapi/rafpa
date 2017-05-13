#!/usr/bin/python

class agentException(Exception):
	message = None
	def __init__(self,**kwargs):
		pass

class SessionCreateError(agentException):
	message = "Hello This is an error"


class deviceConfigReadError(agentException):
	message = "Device Error"
class InvalidLogLevel(agentException):
	message = "Invalid Log Level"
class ConfigPathError(agentException):
	message = "Config path error"
class ScriptsPathError(agentException):
	message = "Scripts path Error"
class AgentRootPathError(agentException):
	message = "Config path missing"
class ConfigError(agentException):
	message = "config error"
class ConfigFileError(agentException):
	message = "Config File Errr"
class HostNameMissing(agentException):
	message = "Host name is missing in configuration file"
class UserNameMissing(agentException):
	message = "User name is missing in configuration file"
class PasswordMissing(agentException):
	message = "Password is missing in configuration file"
class InvalidEntry(agentException):
	message = "Invalid entry in configuration file"
class URIMissing(agentException):
	message = "Missing URI for the attribute"
class ParamMissing(agentException):
	message = "Missing paramater for the attribute"
class ScriptMissing(agentException):
	message = "Missing script for the attribute"
class SessionCreateError(agentException):
	message ="Error in creating session"
class SessionExpired(agentException):
	message = " Session Expired "
class ModuleImportError(agentException):
	message = " Error in importing module"