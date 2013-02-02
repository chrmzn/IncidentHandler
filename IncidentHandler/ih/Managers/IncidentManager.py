import json
import logging
import uuid

from ih.Handlers.IncidentHandler import IncidentHandler
from twisted.web.resource import Resource

class IncidentManager(Resource):

    def __init__(self, tc, config):
        Resource.__init__(self)
        self._tc = tc
        self._config = config
        self._incidentList = {}

    def getChild(self, path, request):
        if path in self._callDetails.keys():
            logging.info("Found incident details for %s", path)
            resp = self._callDetails[path]["Response"]
            return IncidentHandler(resp)
        elif path == "IncomingCall":
            return "Handle a call"
        elif path == "IncomingSMS":
            return "Handle an sms"
        else:
            request.setHeader("Content-Type", "application/json")
            return json.dumps({ "Error" : "Missing key from posted incident message!" })

    def render_POST(self, request):
        request.setHeader("Content-Type", "application/json")
        try:
            logging.info("Recieved Incident Notifier")
            data = json.loads(request.content.getvalue())
            if not "Message" in data:
                return json.dumps({ "Status" : "Failed", "Error" : "Please ensure that you specify a Message" })
            elif not "SMS" in data:
                return json.dumps({ "Status" : "Failed", "Error" : "Please ensure that you specify whether to send SMS or not" })
            elif not "Call" in data:
                return json.dumps({ "Status" : "Failed", "Error" : "Please ensure that you specify whether to send Calls or not" })
            incidentId = str(uuid.uuid4())
            hostname = "ec2-54-246-10-74.eu-west-1.compute.amazonaws.com"
            #respUrl = "http://" + request.getHeader('host') + request.uri + "/" + callId
            respUrl = "http://" + hostname + ":8880" + request.uri + "/" + incidentId
            self._incidentList[callId] = IncidentHandler(data, incidentId, self._tc, self._config)  
            return json.dumps({ "Status" : "Success", "Id" : incidentId})
        except ValueError:
            return json.dumps({ "Status" : "Failed", "Error" : "Could not parse JSON" })
        #except:
        #    return json.dumps({ "Status" : "Failed", "Error" : "Unknown Error..." })
