import logging

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

from ih.Managers.IncidentManager import IncidentManager
from ih.Config.Settings import IncidentConfig
from ih.Handlers.TwilioHandler import TwilioHandler

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    root = Resource()
    config = IncidentConfig()
    tc = TwilioHandler(config._AccountSID, config._AuthToken)

    root.putChild('IncidentManager', IncidentManager(tc, config))

    factory = Site(root)
    reactor.listenTCP(8880, factory)
    reactor.run()

if __name__ == "__main__":
    main()
