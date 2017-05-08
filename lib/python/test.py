#!/usr/bin/python

import Util

confdir="/root/PowerAPI/PowerAPI-Redfish/config"
if __name__ == '__main__':
	Util.LoadSessions(confdir)
	print Util.nodesobj
	n = Util.nodesobj['node3']
	print n.session.expired
	n.createSession()
