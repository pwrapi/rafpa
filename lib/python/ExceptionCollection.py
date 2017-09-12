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
class ValueSetError(agentException):
        message = "Error setting value for the device"
class ResponseSetError(agentException):
        message = "Error setting the param in the response"
class GetConnectionError(agentException):
        message = "Error is Connection"		
