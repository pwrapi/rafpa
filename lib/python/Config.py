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

#This code is to read the configuration for all the objects and attributes
#!/usr/bin/env python

import sys
from os import environ as env,path
import yaml
from Log import Logger
from ExceptionCollection import ConfigPathError,ConfigFileError

log = Logger()

class ConfigParser(object):
	def __init__(self):
		self.config = dict()
	def __iter__(self):
		return iter(self.config)
	def __getitem__(self,key):
		return self.config[key]
	def __setitem__(self,key, value):
		self.config[key] = value
	def keys(self):
		return self.config.keys()
	def values(self):
		return self.config.values()
	def items(self):
		return self.config.items()
	
	
class config(object):
    
    def __init__(self, configfile, configpath=None ):
        
	#  Get the Config File Path from Environment variable
        if configpath == None:
	    configpath = env.get("CONFIG_PATH")
	if configpath == None or not path.isdir(configpath):
	    raise ConfigPathError
	else:
	    log.Debug("CONFIG_PATH: "+configpath)
	    self.configpath = configpath
	try: 	
	    self.config = self.load(configpath+"/"+configfile)
        except IOError as ie:
	    log.Debug(str(ie))
	    self.config = None
	    raise ConfigFileError
	    	
	else:	   	
	    log.Info("Configuration file "+configfile+" loaded. ")	
	    		
    def __del__(self):
		del self.config	
    
    def __enter__(self):
		return self
   
    def __exit__(self,type,value, traceback):
		if value != None:
			raise ConfigFileError


    def load(self,configfile):
		with open(configfile, 'r') as fd:
				yamlConfigDict = yaml.safe_load(fd)
		return  yamlConfigDict

    def __iter__(self):
		return iter(self.config)
		
    def __setitem__(self,key, value):
		try:
			self.config[key]	
		except KeyError as e:
			self.config[key] = value
		else:
			raise IOError

    def __getitem__(self, key):
		return self.config[key]
    
    def keys(self):
		return self.config.keys()
    
    def values(self):
		return self.config.values()
   
    def items(self):
		return self.config.items()
		
