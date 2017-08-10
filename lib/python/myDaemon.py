#!/usr/bin/env python

import sys, time
from daemon import Daemon
import os
import proxy
import argparse

class MyDaemon(Daemon):
        def run(self):
                proxy.main()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', required = False, action='store_true')
	parser.add_argument('path')
	parser.add_argument('opt')
	parser.add_argument('-p', required = False)
	args = parser.parse_args()
	redfish_path = args.path
	foreground = args.f
	operation = args.opt
	port = args.p
        daemon = MyDaemon('/tmp/rafpa.pid',redfish_path)
        if foreground == False and port == None:
                if 'start' == operation:
                        daemon.start()
                        pid = daemon.get_pid()
                        if not pid:
                                print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[91m' + 'FAILED' + '\033[0m' + ']')
                        else:
                                print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
                elif 'stop' == operation:
#                        proxy.loop = 0
                        daemon.stop()
                        proxy.loop = 0
#                        print("RAFPA stopping ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
                elif 'restart' == operation:
                        daemon.restart()
                elif 'status' == operation:
                        daemon.status()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
	elif foreground == False and port != None:
		if 'start' == operation:
			proxy.port = port
			daemon.start()
			pid = daemon.get_pid()
			if not pid:
				print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[91m' + 'FAILED' + '\033[0m' + ']')
			else:
				print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
		elif 'restart' == operation:
			proxy.port = port
			daemon.restart()
		else:
			print "Port parameter(-p) is not using with stop|status operation"
			sys.exit(2)
		sys.exit(0)
	elif foreground == True and port == None:
		if 'start' == operation:
			proxy.main()
		else:
			print "foreground parameter(-f) is only used to start RAFPA service not with stop|status|restart"
			sys.exit(2)
		sys.exit(0)
	elif foreground == True and port != None:
		if 'start' == operation:
			proxy.port = port
			proxy.main()
		else:
			print "foreground parameter(-f) is only used to start RAFPA service not with stop|status|restart"
			sys.exit(2)
		sys.exit(0)
        else:
                print "usage: RAFPA start|stop|restart|status|(start -p <port_num>)"
                sys.exit(2)
