#!/usr/bin/env python
# coding: utf-8
 
import os
import sys
import time
import atexit
import signal
import subprocess
 
 
class Daemon(object):
    """
   A generic daemon class.
 
   Usage: subclass the Daemon class and override the run() method
   """
 
    def __init__(self, pidfile, stdin='/dev/null',
                 stdout='/tmp/out', stderr='/tmp/err'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
 
    def daemonize(self):
        """
       do the UNIX double-fork magic
       """
 
        # Do first fork
        if self.fork() != 0:
            os.waitpid(0, 0)
            time.sleep(0.5)
            return            
 
        # Do second fork
        if self.fork() != 0:
            sys.exit(0)
 
        # Decouple from parent environment
        self.detach_env()
 
        # Flush standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
 
        self.attach_stream('stdin', mode='r')
        self.attach_stream('stdout', mode='a+')
        self.attach_stream('stderr', mode='a+')
 
        # write pidfile
        self.create_pidfile()
 
        # run
        self.run()
        sys.exit(0)
 
 
 
    def attach_stream(self, name, mode):
        """
       Replaces the stream with new one
       """
        stream = open(getattr(self, name), mode)
        os.dup2(stream.fileno(), getattr(sys, name).fileno())
 
    def detach_env(self):
        os.chdir("/root/Git/PowerAPI-Redfish")
        os.setsid()
        os.umask(0)
 
    def fork(self):
        """
       Spawn the child process
       """
        try:
            return os.fork()
        except OSError as e:
            sys.stderr.write("Fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)
 
    def create_pidfile(self):
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("%s\n" % pid)
 
    def delpid(self):
        """
       Removes the pidfile on process exit
       """
        os.remove(self.pidfile)

    def kill_child_process(self):
		parent_pid = self.get_pid()
		ps_command = subprocess.Popen("ps -o pid --ppid %d --noheaders" % parent_pid, shell=True, stdout=subprocess.PIPE)
		ps_output = ps_command.stdout.read()
#		print (ps_output)
		retcode = ps_command.wait()
		if (ps_output != ''):
		    for pid_str in ps_output.strip().split("\n"):
#		        print (int(pid_str))
		        os.kill(int(pid_str), signal.SIGTERM)
#		sys.exit()

    def start(self):
        """
       Start the daemon
       """
        # Check for a pidfile to see if the daemon already runs
        pid = self.get_pid()
 
        if pid:
            message = "RAFPA (pid %s) is already" + '\033[92m' + '\033[1m' + ' running ...' + '\033[0m' + '\n'
            sys.stderr.write(message % pid)
            sys.exit(1)
 
        # Start the daemon
        self.daemonize()
 
    def get_pid(self):
        """
       Returns the PID from pidfile
       """
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except (IOError, TypeError):
            pid = None
        return pid
 
    def stop(self, silent=False):
        """
       Stop the daemon
       """
        # Get the pid from the pidfile
        pid = self.get_pid()
 
        if not pid:
            if not silent:
                message = "RAFPA daemon is" '\033[92m' + '\033[91m' + ' not running' + '\033[0m' + '\n'
                sys.stderr.write(message)
            return # not an error in a restart
 
#        signal.signal(signal.SIGTERM, kill_child_process)
        self.kill_child_process()
        # Try killing the daemon process
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stdout.write(str(err))
                sys.exit(1)
        print("RAFPA stopping ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']') 
    def restart(self):
        """
       Restart the daemon
       """
        self.stop(silent=True)
# print("RAFPA stopping ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
        self.start()
#        print("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')
        pid = self.get_pid()
        if not pid:
            print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[91m' + 'FAILED' + '\033[0m' + ']' + '\n')
        else:
            print ("RAFPA starting ..." + "\t\t" + '[' + '\033[92m' + '\033[1m' + 'OK' + '\033[0m' + ']')

    def status(self):
	"""
     	Check the status of the daemon
     	"""
     	pid = self.get_pid()

     	if pid:
     	   message = "RAFPA (pid %s) is " + '\033[92m' + '\033[1m' + ' running ...' + '\033[0m' + '\n'
           sys.stderr.write(message % pid)
        else:
            print("RAFPA daemon is" '\033[92m' + '\033[91m' + ' not running' + '\033[0m' + '\n')
            

 
    def run(self):
        """
       You should override this method when you subclass Daemon. It will be called after the process has been
       daemonized by start() or restart().
       """
        raise NotImplementedError
