import json
import logging

from twisted.web.resource import Resource
from apscheduler.scheduler import Scheduler

class IncidentHandler(Resource):

    def __init__(self, incidentDetails, incidentId, tc, config):
        self._incidentDetails = incidentDetails
        self._incidentId = incidentId
        self._tc = tc
        self._config = config
        self._Sched = Scheduler()

        self._notifcationState = {}

        self._beginNotifications()

    def _beginNotifications(self):
        logging.info("Beginning notification process")
        if self._incidentDetails["SMS"].lower() == "true":
            self._notificationState["SMS"] = {}
            logging.info("Incident is set to send SMS messages, generating an ID for text message response")
            self._smsPin = self.generate_pins(4, 1) 
            smsMessage = self._incidentDetails["Message"] + "\nPlease respond with the PIN: %s to accept this ticket" % str(self._smsPin))
            logging.info("Pin is set to %s" % str(self._smsPin))
            for user in self._config.Users():
                if user["SMS"] == "True":
                    res = self._tc.sendMessage(self._config.TwilioNumber(), user["Phone"], smsMessage)
                    
                   
            

    def render_GET(self, request):
        logging.info("Call responder: " + ", ".join(request.postpath))
        return self._respData

    #http://stackoverflow.com/questions/1436552/unique-pin-generator
    def generate_pins(length, count, alphabet=string.digits):
        alphabet = ''.join(set(alphabet))
        if count > len(alphabet)**length:
            raise ValueError("Can't generate more than %s > %s pins of length %d out of %r" %
                             count, len(alphabet)**length, length, alphabet)
       def onepin(length):
           return ''.join(random.choice(alphabet) for x in xrange(length))
       result = set(onepin(length) for x in xrange(count))
       while len(result) < count:
           result.add(onepin(length))
       return list(result)

