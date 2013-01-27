import json

class IncidentHandler(Resource):

    def __init__(self, tc):
        Resource.__init__(self)
        self._tc = tc
        self._callDetails = {}

    def getChild(self, path, request):
        if path in self._callDetails.keys():
            logging.info("Found call details for %s", path)
            resp = self._callDetails[path]["Response"]
            del self._callDetails[path]
            return CallResponder(resp)

    def render_GET(self, request):
        return "<html><body>%s</body></html>" % (time.ctime(),)

    def render_POST(self, request):
        try:
            logging.info("Recieved Incident Notifier")
            data = json.loads(request.content.getvalue())
            callId = str(uuid.uuid4())
            hostname = "ec2-54-246-10-74.eu-west-1.compute.amazonaws.com"
            #respUrl = "http://" + request.getHeader('host') + request.uri + "/" + callId
            respUrl = "http://" + hostname + ":8880" + request.uri + "/" + callId
            self._callDetails[callId] = { "Response" : str(ResponseParser(data['Response']))}
            res = self._tc.sendCall(data['From'], data['To'], respUrl)
            sid = res.sid
            pprint.pprint(self._callDetails)
            return "<html><body>Successfully sent call - ID: %s</body></html>\n" % (str(sid),)
        except KeyError:
            return json.dumps({ "Error" : "Missing key from incident message!" })
        except ValueError:
            return json.dumps({ "Error" : "Could not parse JSON" })
        return "<html><body><pre>%s</pre></body></html>\n"

