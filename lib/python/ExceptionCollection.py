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
class AttrGetError(agentException):
    message = "Error getting attribute from database"
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
class SessionGetError(agentException):
    message = "Error in getting Session info"
class ModuleImportError(agentException):
	message = " Error in importing module"
class ValueGetError(agentException):
	message = " Error in getting Value from device"

class SocketError(agentException):
    message = "Error in creating the socket"
class URLGetError(agentException):
        message = "Error getting URL from Device"
class ParamGetError(agentException):
        message = "Error getting Param from Device"
class DynamicURLCreateError(agentException):
        message = "Error creating dynamic url for the Device"
class ParamInResponseGetError(agentException):
        message = "Error getting the param in the response"	
