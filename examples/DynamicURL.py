import string

URL="/redfish/v1/Chassis/$Chassis&/CPU/$CPU&/dimm/proc$CPU&dimm$dimm&"
entity ="Chassis#1.CPU#2.dimm#8"
entities = entity.split(".")
newlist=[]
for ents in entities:
    newlist.append(ents.split("#"))

entDic = dict(newlist)

newURL=''

for key in entDic:
    
    if key in URL:
        replacestring = "$" + key + "&"
        newURL = string.replace(URL,replacestring,entDic[key])
        URL = newURL
print URL            

    	

