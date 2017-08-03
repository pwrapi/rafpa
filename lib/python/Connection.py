import os
import sys
import socket
from multiprocessing import Process, Queue
import Util
from ExceptionCollection import ValueGetError,SocketError
from time import sleep
from random import randint

from Log import Logger
log = Logger()

'''
This Module handles system specific Socket handling functions
'''

class Connection:

    SOCKET_IO_ERROR = None
    SOCKET_UNKNOWN_ERROR = None
    SUCCESS = 0


    def __init__(self, hostname="0.0.0.0", port=8080):

        # verify the host name.
        # If no host name available. get the host name from config
        # Get the port number if not mentioned get the port number from config
        # All initialization for the connection
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(None)
            self.socket.bind((hostname, port))

        except IOError as ior:
            # Set the Error Flag appropriately
            Connection.SOCKET_IO_ERROR = True
        except Exception as unknown:
            # Set the Error Flag appropriately
            Connection.SOCKET_UNKNOWN_ERROR = True
        return
    def __del__(self):
        log.Info("Closing the connection..")
        self.socket.close()

    def daemonize(self):
        pass

    def start_listener(self,num_conn=0):
        # Create socket.
        # Check for error conditions.
        # Set approproate errors
        # Raise exceptions if required.
        # return socket or Error conditions
        try:
            self.socket.setblocking(False)
            self.socket.listen(num_conn)
            # add a watcher here also whenever socket connection expires of the entries . This should be renewed
        except IOError as ior:
            # Set the Error Flag appropriately
            log.Error("Error in creating the Socket {0}".format(ior))
            raise SocketError
        except Exception as unknown:
            # Set the Error Flag appropriately
            log.Error("Unknown Error while creating the socket {0}".format(unknown))
            raise SocketError

        return

    def stop_listener(self):
        self.socket.close()
    def cleanup(self):
        pass

    def connection_handler(self):
        data = []

        string = str()
        self.socket.setblocking(True)
        c, addr = self.socket.accept()
        t = handler(c)
        p = Process(target=t.run,args=())
        p.start()


class handler(object):
    def __init__(self, socket):
        self.socket = socket

    def run(self):
        index = 0
        c = self.socket
        data = str()
        
        while True:
            buffer = c.recv(50)
            if len(buffer) == 0:
                return
            data += buffer.strip()
            index = data.find(";")
            if index < 0:
                next

            try:
                command_str = data[0:index]
                data = data[index+1:]
            except IndexError as e:
                data = []
            index = command_str.find(":")
            if index < 0:
                c.send("NO_OP")
            
            command = command_str[:index]
            if command == "get":
                value = self.get(command_str[index+1:])
                c.send(str(value))
                
            elif command == "set":
                value = self.set( command_str[index+1:] )
                c.send(str(value))
                
            else:
                c.send("NO_OP")
        
        return

    def get(self, string):
        entity,redfish_host,device_name,attr = None,None,None,None
        try:
            entity,redfish_host,device_name,attr = string.split(":")
            if entity == None or redfish_host == None or \
                device_name == None or attr == None:
                log.Error("Error in passing one of the data , redfish host, entity, device name or attribute") 
                raise ValueGetError    
            query_device = device_name.rsplit(".")[-1]
            query_device = query_device.split('#')[0]

            handler = Util.gethandler(entity, query_device, attr)
        except Exception as e:
            log.Error(e) 
            log.Error("Error getting handler for {ent} {device} {attr_name}".format(ent=entity,device=device_name,attr_name=attr))
            return -1
        try:
            node = Util.getNode(redfish_host)
            session = node.getSession().get()
        except Exception as e:
            log.Error(e)
            log.Error("Error getting session for node {0}".format(redfish_host))
            return -1
        try:
            value = handler.get(session,entity, device_name, attr)
#print "----------------------"+value+"------------------\n";
        except Exception as e:
            log.Error("Error getting value from handler for {0} {1} {2} {3} ".format(type(handler),entity,device_name,attr))
            return -1    
        return value
    
    def set(self, string):
        entity,redfish_host,device_name,attr,command = None,None,None,None,None
        try:
            entity,redfish_host,device_name,attr,command = string.split(":")
            if entity == None or redfish_host == None or \
                device_name == None or attr == None or command == None:
                log.Error("Error in passing one of the data , redfish host, entity, device name or attribute") 
                raise ValueGetError    
            query_device = device_name.rsplit(".")[-1]
            query_device = query_device.split('#')[0]

            handler = Util.gethandler(entity, query_device, attr)
        except Exception as e:
            log.Error(e) 
            log.Error("Error getting handler for {ent} {device} {attr_name}".format(ent=entity,device=device_name,attr_name=attr))
            return -1
        try:
            node = Util.getNode(redfish_host)
            session = node.getSession().get()
        except Exception as e:
            log.Error(e)
            log.Error("Error getting session for node {0}".format(redfish_host))
            return -1
        try:
            value = handler.set(session,entity, device_name, attr,command)
#print "----------------------"+value+"------------------\n";
        except Exception as e:
            log.Error("Error getting value from handler for {0} {1} {2} {3} ".format(type(handler),entity,device_name,attr))
            return -1    
        return value

    
