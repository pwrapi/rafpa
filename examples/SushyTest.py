from sys import path
path.insert(0,"/root/Git/PowerAPI-Redfish/lib/python")
import Util
from Log import Logger,Log
import json

log = Logger(Log.ERROR)
path.append("/root/Git/PowerAPI-Redfish/scripts")
cp=Util.get_config_path()
Util.LoadConfiguration(cp)
co=Util.getConfigObj()
#print co

dev = co['ilo4']['chassis']
#print dev

att = dev['AvgPower']
att.load(dev)
#obj = att.getmodobj()
#print obj
#URL = att.getURL()
URL1 = Util.getURL('ilo4','chassis#1','AvgPower','get')		
print URL1
URL2 = Util.getURL('ilo4','chassis#1','AvgPower','set')
print URL2


Param1 = Util.getParam('ilo4','chassis#1','AvgPower','get')		
print Param1
Param2 = Util.getParam('ilo4','chassis#1','AvgPower','set')
print Param2

'''		
Util.LoadSessions(cp)
nodenames = Util.getNodeNames()
nodesobj = Util.getNodesobj()
print nodesobj

for nodename in nodenames:
    node = nodesobj[nodename]
    node.createSession()	
	


node = Util.getNode("node2")
sushyobj2 = node.getSession().get()

node = Util.getNode("node3")
sushyobj3 = node.getSession().get()
print sushyobj3



value1 = restobj.get(URL1)
print value1		
		
json_data1 = json.loads(value1.text)
		
print json_data1

print json_data1[Param]

    
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
'''


    
