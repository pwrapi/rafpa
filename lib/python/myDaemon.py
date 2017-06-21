#!/usr/bin/env python

import sys, time
from daemon import Daemon
import os
import proxy

class MyDaemon(Daemon):
        def run(self):
                proxy.main()

if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                        pid = daemon.get_pid()
                        if not pid:
                                print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[91m' + 'FAILED' + '\033[0m' + ']')
                        else:
                                print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
                elif 'stop' == sys.argv[1]:
#                        proxy.loop = 0
                        daemon.stop()
                        proxy.loop = 0
#                        print("RAFPA stopping ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                elif 'status' == sys.argv[1]:
                        daemon.status()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart|status" % sys.argv[0]
                sys.exit(2)
