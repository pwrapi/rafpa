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

from Config import config as con
from Config import ConfigParser
from time import time
from ExceptionCollection import HostNameMissing,UserNameMissing,PasswordMissing,InvalidEntry,SessionCreateError
from Log import Logger

log = Logger()


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
            

import Util
class Node(object):

    def __init__(self,name):
        self.name = name
        self.active = False
        self.session = Session()
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
    
    def createSession(self):
        retries = 1    
        while retries < 3:    
            try:
                log.Info("Connecting to server {host} with {user} try {tries}".format(host=self.hostname, user=self.username,tries=retries))
                
		if self.hostname =="localhost" :
                    session = Util.redfish_server_login(self.hostname,self.username,self.password)
                else :
                    session = Util.sushy_server_login(self.hostname,self.username,self.password)
	        '''
		session = Util.sushy_server_login(self.hostname,self.username,self.password)
	        '''
            except Exception as e:
                log.Error(e)
                retries += 1
            else:
                self.storeSessionInfo(session)
                self.setActive(True)
                break
        else:
            log.Error("Connecting to server {host} with {user} exhausted number of tries {tries} ".format(host=self.hostname,user=self.username,tries=retries))    
            self.setActive(False)
            raise SessionCreateError
            

    def storeSessionInfo(self, session, time=time()):
        self.session.set(session,time)
            
        
    def getSession(self):
        return self.session

    def isActive(self):
        return self.active
    def setActive(self, state):    
        self.active = state

class Session():
    def __init__(self):
        self.session = None
        self.expired= True
    def set(self,session, time= time()):    
        self.session = session
        self.start = time
        self.elapsed = 0
        self.expired = False        
    def __del__(self):
        # Log out of the session
        # Mark Session as expired
        pass

    def get(self):
#       log.Debug("Returning session information")
#log.Debug(self.session)
        if self.expired:
            log.Error("Session expired")
            raise SessionExpired
        else:
            log.Debug("Session active. Returning the session information")
            return self.session
