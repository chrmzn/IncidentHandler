#!/usr/bin/env python

import ConfigParser
import os
import logging
import pprint

class IncidentConfig(object):

    _homeFolder = os.environ["HOME"] + os.path.sep + ".incidentHandler"
    _configPath = _homeFolder + os.path.sep + "settings.cfg"

    def __init__(self):
        if not os.path.exists(self._configPath):
            self._createConfig()
        else:
            self._readConfig()
    
    def _createConfig(self):
        config = ConfigParser.SafeConfigParser()
        config.add_section("Twilio")

        print "Enter in your Twilio Account SID"
        sid = raw_input('---> ')
        config.set("Twilio", "AccountSID", sid)
        self._AccountSID = sid

        print "Enter in your Twilio Auth Token"
        token = raw_input('---> ')
        config.set("Twilio", "AuthToken", token)
        self._AuthToken = token

        print "Enter in your Twilio Phone Number"
        token = raw_input('---> ')
        config.set("Twilio", "TwilioNumber", twn)
        self._TwilioNumber = twn

        print "How many users would you like to setup...."
        users = raw_input('---> ')
        self._Users = []

        try:
            users = int(users)
        except ValueError:
            logging.info("User did not specify a valid integer")

        while not type(users) == int:
            try:
                print "Please specify a valid integer..."
                users = raw_input('---> ')
                users = int(users)
            except ValueError:
                logging.info("User did not specify a valid integer")
                continue

        for num in range(users):
            userno = "User-" + str(num)
            logging.info("Adding a section for user number: " + str(num))
            config.add_section(userno)
    
            name = raw_input("Full Name: ")
            while name == "":
                name = raw_input("Full Name: ")
            config.set(userno, "Name", name)

            phone = raw_input("Phone Number (Eg. +447545231671): ")
            while phone == "":
                phone = raw_input("Phone Number (Eg. +447545231671): ")
            config.set(userno, "Phone", phone)

            smsReceive = self.trueFalseResponse("Should user receive SMS? [y]: ", True)
            config.set(userno, "SMS", str(smsReceive))

            callReceive = self.trueFalseResponse("Should user receive Calls? [y]: ", True)
            config.set(userno, "Call", str(callReceive))
            self._Users.append({ "Name" : name, "Phone" : phone, "SMS" : smsReceive, "Call" : callReceive })

        if not os.path.exists(self._homeFolder):
            os.mkdir(self._homeFolder)
        
        with open(self._configPath, 'wb') as configfile:
            config.write(configfile)

    def _readConfig(self):
        config = ConfigParser.SafeConfigParser()
        config.read(self._configPath)
        self._AccountSID = config.get("Twilio", "AccountSID")
        self._AuthToken = config.get("Twilio", "AuthToken")
        self._TwilioNumber = config.get("Twilio", "TwilioNumber")
        self._Users = []
        userIterator = 0
        while config.has_section("User-%s" % (userIterator,)):
            try:
                self._Users.append({ 
                                     "Name"  : config.get("User-%s" % (userIterator,), "Name"),
                                     "Phone" : config.get("User-%s" % (userIterator,), "Phone"),
                                     "SMS"   : config.get("User-%s" % (userIterator,), "SMS"),
                                     "Call"  : config.get("User-%s" % (userIterator,), "Call")
                                   })
            except ConfigParser.NoSectionError:
                logging.warn("User %s config section was incomplete...ignoring" % (userIterator,))
            userIterator += 1
        pprint.pprint(self._Users)

    def trueFalseResponse(self, query, default=None):
        rawIn = raw_input(query)
        if (default == True or default == False) and rawIn == "":
            return default

        while not rawIn.lower() in ['y', 'yes', 'n', 'no', 'true', 'false']:
            rawIn = raw_input("Please specify yes, no, y, n, true or false: ")
    
        if rawIn.lower() in ['y', 'yes', 'true']:
            return True
        else:
            return False

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    ic = IncidentConfig()
