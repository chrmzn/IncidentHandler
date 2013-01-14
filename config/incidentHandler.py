#!/usr/bin/env python

import ConfigParser
import os
import logging

def trueFalseResponse(query, default=None):
    rawIn = raw_input(query)
    if (default == True or default == False) and rawIn == "":
        return default

    while not rawIn.lower() in ['y', 'yes', 'n', 'no', 'true', 'false']:
        rawIn = raw_input("Please specify yes, no, y, n, true or false: ")

    if rawIn.lower() in ['y', 'yes', 'true']:
        return True
    else:
        return False

logging.basicConfig(level=logging.DEBUG)

homeFolder = os.environ["HOME"] + os.path.sep + ".incidentHandler" 
configPath = homeFolder + os.path.sep + "settings.cfg"

if not os.path.exists(configPath):
    config = ConfigParser.SafeConfigParser()
    config.add_section("Twilio")
    
    print "Enter in your Twilio Account SID"
    sid = raw_input('---> ')
    config.set("Twilio", "AccountSID", sid)
    
    print "Enter in your Twilio Auth Token"
    token = raw_input('---> ')
    config.set("Twilio", "AuthToken", token)

    print "How many users would you like to setup...."
    users = raw_input('---> ')

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
        
        smsReceive = trueFalseResponse("Should user receive SMS? [y]: ", True) 
        config.set(userno, "SMS", str(smsReceive))

        callReceive = trueFalseResponse("Should user receive Calls? [y]: ", True) 
        config.set(userno, "Call", str(callReceive))

    if not os.path.exists(homeFolder):
        os.mkdir(homeFolder)

#    with open(configPath, 'wb') as configfile:
#        config.write(configfile)

        
