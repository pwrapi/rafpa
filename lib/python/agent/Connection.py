import os
import sys
import socket
from multiprocessing import Process, Queue
import Util
import Exceptions as Execs
from time import sleep
from random import randint
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
            Execs.SocketErrorHandler(ior)
	    raise IOError	
        except Exception as unknown:
            # Set the Error Flag appropriately
            Execs.UnknownException(unknown)

        return

    def stop_listener(self):
        self.socket.close()
    def cleanup(self):
        pass

    def connection_handler(self,config,sessions,objs,ts):
        data = []

        string = str()
        self.socket.setblocking(True)
        c, addr = self.socket.accept()
	t = handler(c,config,sessions,objs)
	p = Process(target=t.run,args=())
	print "started the the process"
	p.start()


class handler(object):
	def __init__(self, socket,config,sessions,objs):
		self.socket = socket
		self.config = config
		self.sessions = sessions
		self.objs = objs
	def run(self):
		index = 0
		c = self.socket
		config = self.config
		sessions = self.sessions
		objs = self.objs
	
		data = str()
		
		while True:
		
			buffer = c.recv(50)
			if len(buffer) == 0:
				return
			data += buffer.strip()
			index = data.find(";")
			if index < 0:
				next
			command_str = data[0:index]
			try:
				data = data[index+1:]
			except IndexError as e:
				data = []
			index = command_str.find(":")
			if index < 0:
				c.send("NO_OP")
			
			command = command_str[:index]
			if command == "get":
				value = self.get(config, sessions, objs, command_str[index+1:])
				c.send(str(value))
				
			elif command == "put":
				value = put(config, command_str[inex+1:])
				c.send(str(value))
				
			else:
				c.send("NO_OP")
		
		return

	def get(self,config, sessions, objs,string):
		entity,redfish_host,device_name,attr = string.split(":")
		handle_name = Util.gethandler(config,entity, device_name)
		
		if handle_name == None:
			retrun -1
		try:	
			handler = objs[handle_name]
		except KeyError as k:
			print k
			return -1	
		try:
			value = handler.get(entity, redfish_host, device_name, attr)
		except Exception as e:
			print e	
			return -1	
		return value
	

	def put(self, config, objs,string):
	
		entity,redfish_host,device_name,attr,command = string.split(":")
		handle_name = Util.gethandler(entity, device_name)
		if handle_name == None:
			return -1
		try:
			handler = objs[handle_name]
		except KeyError as k:
			return -1
		try:	
			status = handler.put(entity, redfish_host, device_name, attr,command)
		except Exception as e:
			return -1
		return status


