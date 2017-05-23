from sys import path
path.insert(0,"/root/PowerAPI_Code/PowerAPI-Redfish/lib/python")
import Util
from Log import Logger,Log
import json

log = Logger(Log.ERROR)
path.append("/root/PowerAPI_Code/PowerAPI-Redfish/scripts")
cp=Util.get_config_path()
Util.LoadConfiguration(cp)
co=Util.getConfigObj()
#print co
dev = co['ilo4']['Chassis']
att = dev['AvgPower']
att.load(dev)
#obj = att.getmodobj()
#print obj
URL = att.getURL()
#print URL
Param = att.getParam()
#print Param
Util.LoadSessions(cp)
nodenames = Util.getNodeNames()
nodesobj = Util.getNodesobj()
#print nodesobj

for nodename in nodenames:
    node = nodesobj[nodename]
    node.createSession()	
	
node = Util.getNode("node0")
sushyobj1 = node.getSession().get()

node = Util.getNode("node2")
sushyobj2 = node.getSession().get()

node = Util.getNode("node3")
sushyobj3 = node.getSession().get()


value1 = sushyobj1.get(URL)
json_data1 = json.loads(value1.text)

if Param not in json_data1:
    print "no"
else:
    b = json_data1[Param]
    print b

    
value2 = sushyobj2.get(URL)
json_data2 = json.loads(value2.text)	
if Param not in json_data2:
    print "no"
else:
    b = json_data2[Param]
    print b

value3 = sushyobj3.get(URL)
json_data3 = json.loads(value3.text)	
if Param not in json_data3:
    print "no"
else:
    b = json_data3[Param]
    print b



    
