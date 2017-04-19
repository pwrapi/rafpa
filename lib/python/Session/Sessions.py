#this class is to create sessions and return restoject

import sys
from _restobject import RestObject


class sessions(object):
    dic ={}       
    restobj = ""
    """
    def __init__(self,iloname,iloIP,username,password,nodelist):
        self.iloname = iloname
        self.iloIP = iloIP
        self.username = username
        self.password = password
        self.nodelist = nodelist
        #self.dic = dic
    """
    def __init__(self):
        pass
        
    def createSession(self,iloip,username,password,node):
        try:
            #print self.nodelist
	    print "{0} {1} {2} {3}".format(iloip,username,password,node)
            REST_OBJ = self.getRestObject(node,iloip,username,password)
                #print REST_OBJ
            self.dic[node] = REST_OBJ

            
            return self.dic
        except Exception as e:
            raise e
            
            
    def getRestObject(self,node,iloip,username,password):
        try:
            if node == "local" :
                 iLO_https_url = "blobstore://."
                 iLO_account = "None"
                 iLO_password = "None"
            else:
                 iLO_https_url = "https://"+ iloip
                 iLO_account = username
                 iLO_password = password


            self.restobj = RestObject(iLO_https_url, iLO_account, iLO_password)
            return self.restobj
        except Exception as e:
            raise e
               
            
    
