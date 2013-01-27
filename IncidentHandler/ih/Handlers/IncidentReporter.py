
import json
import logging

from twisted.web.resource import Resource

class IncidentReporter(Resource):

    def __init__(self, tc):
        Resource.__init__(self)
        self._tc = tc
        self._incidents = {}

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
            data = json.loads(request.content.getvalue())
        except ValueError:
            logging.warn("Issues loading the JSON posted to the server returning error...")
            return json.dumps({ "Error" : "Unable to load the json posted to the server!" }) 
        incidentId = str(uuid.uuid4())
        hostname = "ec2-54-246-10-74.eu-west-1.compute.amazonaws.com"
        #respUrl = "http://" + request.getHeader('host') + request.uri + "/" + callId
        respUrl = "http://" + hostname + ":8880" + request.uri + "/" + callId

        self._incidents[incidentId] = { "Response" : str(ResponseParser(data['Response']))}
        res = self._tc.sendCall(data['From'], data['To'], respUrl)
        sid = res.sid
        pprint.pprint(self._callDetails)
        return "<html><body>Successfully sent call - ID: %s</body></html>\n" % (str(sid),)


