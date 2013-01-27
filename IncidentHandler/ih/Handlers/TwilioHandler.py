import logging

from twilio.rest import TwilioRestClient

class TwilioHandler():

    def __init__(self, account, auth):
        self._account_sid = account
        self._auth_token = auth
        self._authenticate()

    def _authenticate(self):
        logging.info("Authenticating to Twilio")
        self._client = TwilioRestClient(self._account_sid, self._auth_token)

    def sendMessage(self, src, dst, body):
        logging.info("Sending Twilio Message")
        return self._client.sms.messages.create(body=body, to=dst, from_=src)

    def sendCall(self, src, dst, url):
        logging.info("Sending Twilio Call")
        return self._client.calls.create(url=url, to=dst, from_=src, method="GET")
