#this object is used to connect to ilorest client for inband communication
import sys
import json
from Log import Logger

from redfish import AuthMethod, rest_client

log = Logger()
log.Info("Connecting to Ilorest for inband Communication")	



class RestObject(object):
    def __init__(self, host, login_account, login_password):
        self.rest_client = rest_client(base_url=host, \
                          username=login_account, password=login_password, \
                          default_prefix="/redfish/v1")
        self.rest_client.login(auth=AuthMethod.SESSION)

    def __del__(self):
        self.rest_client.logout()

    def search_for_type(self, type):
        instances = []

        for item in self.SYSTEMS_RESOURCES["resources"]:
            foundsettings = False

            if type and type.lower() in item["Type"].lower():
                for entry in self.SYSTEMS_RESOURCES["resources"]:
                    if (item["href"] + "/settings").lower() == \
                                                        (entry["href"]).lower():
                        foundsettings = True

                if not foundsettings:
                    instances.append(item)

        if not instances:
            sys.stderr.write("\t'%s' resource or feature is not " \
                                            "supported on this system\n" % type)
        return instances

    def error_handler(self, response):
        if not self.MESSAGE_REGISTRIES:
            sys.stderr.write("ERROR: No message registries found.")

        try:
            message = json.loads(response.text)
            newmessage = message["Messages"][0]["MessageID"].split(".")
        except:
            sys.stdout.write("\tNo extended error information returned by " \
                                                                    "iLO.\n")
            return

        for err_mesg in self.MESSAGE_REGISTRIES:
            if err_mesg != newmessage[0]:
                continue
            else:
                for err_entry in self.MESSAGE_REGISTRIES[err_mesg]:
                    if err_entry == newmessage[3]:
                        sys.stdout.write("\tiLO return code %s: %s\n" % (\
                                   message["Messages"][0]["MessageID"], \
                                   self.MESSAGE_REGISTRIES[err_mesg][err_entry]\
                                   ["Description"]))

    def rest_get(self, suburi):
        """REST GET"""
        return self.rest_client.get(path=suburi)

    def rest_patch(self, suburi, request_body, optionalpassword=None):
        """REST PATCH"""
        sys.stdout.write("PATCH " + str(request_body) + " to " + suburi + "\n")
        response = self.rest_client.patch(path=suburi, body=request_body, \
                                            optionalpassword=optionalpassword)
        sys.stdout.write("PATCH response = " + str(response.status) + "\n")

        return response

    def rest_put(self, suburi, request_body, optionalpassword=None):
        """REST PUT"""
        sys.stdout.write("PUT " + str(request_body) + " to " + suburi + "\n")
        response = self.rest_client.put(path=suburi, body=request_body, \
                                            optionalpassword=optionalpassword)
        sys.stdout.write("PUT response = " + str(response.status) + "\n")

        return response


    def rest_post(self, suburi, request_body):
        """REST POST"""
        sys.stdout.write("POST " + str(request_body) + " to " + suburi + "\n")
        response = self.rest_client.post(path=suburi, body=request_body)
        sys.stdout.write("POST response = " + str(response.status) + "\n")

        return response


    def rest_delete(self, suburi):
        """REST DELETE"""
        sys.stdout.write("DELETE " + suburi + "\n")
        response = self.rest_client.delete(path=suburi)
        sys.stdout.write("DELETE response = " + str(response.status) + "\n")

        return response
    


