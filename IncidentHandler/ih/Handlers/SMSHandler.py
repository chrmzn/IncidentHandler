


class SMSHandler(Resource):
    isLeaf = True
    def __init__(self, msgClient):
        Resource.__init__(self)
        self._msgClient = msgClient

    def render_GET(self, request):
        return "<html><body>%s</body></html>" % (time.ctime(),)

    def render_POST(self, request):
        try:
            data = json.loads(request.content.getvalue())
            res = self._msgClient.sendMessage(data['From'], data['To'], data['Message'], url='http://ec2-54-246-10-74.eu-west-1.compute.amazonaws.com:8880/responder')
            sid = res.sid
            return "<html><body>Successfully Parsed JSON %s</body></html>\n" % (str(sid),)
        except ValueError:
            return "<html><body>Failed to parse JSON</body></html>\n"
        return "<html><body><pre>%s</pre></body></html>\n"
