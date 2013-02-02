import json
import logging
import datetime

from twisted.web.resource import Resource
from apscheduler.scheduler import Scheduler
from ih.Parsers.ResponseParser import ResponseParser as rp

class IncidentHandler(Resource):

    def __init__(self, incidentDetails, incidentId, tc, config):
        self._incidentDetails = incidentDetails
        self._incidentId = incidentId
        self._tc = tc
        self._config = config
        self._Sched = Scheduler()
        self._Sched.start()

        self._notifcationState = {}

        self._beginNotifications()

    def _beginNotifications(self):
        logging.info("Beginning notification process")
        if self._incidentDetails["SMS"].lower() == "true":
            self._notificationState["SMS"] = {}
            self._sendSMS()
        if self._incidentDetails["Call"].lower() == "true" and self._incidentDetails["SMS"].lower() == "true" :
            self._notificationState["Call"] = {}
            logging.info("Beginning calls in 5 minutes time")
            self._callJob = self._Sched.add_date_job(self._sendCalls, (datetime.datetime.now() - datetime.timedelta(minutes=5)))
        elif self._incidentDetails["Call"].lower() == "true":
            self._sendCalls()
    
    def _sendSMS(self):
        logging.info("Incident is set to send SMS messages, generating an ID for text message response")
        self._smsPin = self.generate_pins(4, 1)
        smsMessage = self._incidentDetails["Message"] + "\nPlease respond with the PIN: %s to accept this ticket" % str(self._smsPin))
        logging.info("SMS Pin is set to %s" % str(self._smsPin))
        self._incidentDetails["SMS_Pin"] = self._smsPin
        for user in self._config.Users():
            if user["SMS"] == "True":
                logging.info("User '%s' is set to recieve SMS messages...Sending..." % user["Name"])
                res = self._tc.sendMessage(from_=self._config.TwilioNumber(), 
                                           to=user["Phone"], 
                                           body=smsMessage)
            else:
                logging.info("User '%s' is not set to recieve SMS messages...Skipping..." % user["Name"])

    def _sendCalls(self):
        logging.info("Incident is set to send SMS messages, generating an ID for text message response")
        self._callPin = self.generate_pins(4, 1)
        logging.info("Call Pin is set to %s" % str(self._smsPin))
        responseArray = [{ "Say" : "New Incident"},
                         { "Say" : self._incidentDetails["Message"]},
                         { "Gather" : { "say"         : "Please key the following digits to accept the task " + str(self._callPin),
                                        "action"      : "http://host:port/IncidentHandler/Id/PinCheck",
                                        "method"      : "GET",
                                        "finishOnKey" : "*"},
                         { "Say" : "You entered no digits. Goodbye!"}]
        responseArray = rp(responseArray)
        for user in self._config.Users():
            if user["Call"] == "True":
                logging.info("User '%s' is set to recieve calls...Sending..." % user["Name"])
                res = self._tc.sendCall(from_=self._config.TwilioNumber(), 
                                        to=user["Phone"], 
                                        url="http://host:port/IncidentHandler/Id/CallResponse")
            else:
                logging.info("User '%s' is not set to recieve calls...Skipping..." % user["Name"])
        
    def getSMSPin(self):
        return self._smsPin
        
    def getCallPin(self):
        return self._callPin

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

