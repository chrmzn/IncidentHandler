import twilio.twiml

class ResponseParser():

    def __init__(self, respArray):
        logging.info("Building response object")
        self._twilioData = twilio.twiml.Response()
        self._parseArray(respArray)

    def _parseArray(self, respArray):
        for resp in respArray:
            if resp.keys()[0] == "Say":
                self._twilioData.say(resp.values()[0])

    def __str__(self):
        return str(self._twilioData)
