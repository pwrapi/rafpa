from sys import path
path.insert(0,"/root/PowerAPI_Code/PowerAPI-Redfish/lib/python")
import Util
from Log import Logger,Log

log = Logger(Log.DEBUG)
path.append("/root/PowerAPI_Code/PowerAPI-Redfish/scripts")
cp=Util.get_config_path()
Util.LoadConfiguration(cp)
co=Util.getConfigObj()
print co
dev = co['ilo4']['Chassis']
att = dev['AvgPower']
att.load(dev)
#obj = att.getmodobj()
#print obj
URL = att.getURL()
print URL
Param = att.getParam()
print Param
Util.LoadSessions(cp)
nodenames = Util.getNodeNames()
nodesobj = Util.getNodesobj()
print nodesobj

for nodename in nodenames:
    node = nodesobj[nodename]
    node.createSession()	

print nodesobj	
node = Util.getNode("node3")
sushyobj1 = node.getSession().get()

node = Util.getNode("node2")
sushyobj2 = node.getSession().get()

if sushyobj1 is sushyobj2:
    print "Yes"
print dir(sushyobj1)
print dir(sushyobj2)

value = sushyobj1.get_system(URL)
if Param not in value.json:
    print "no"
else:
    b = value.json[Param]
    print b
#obj.get(None)
