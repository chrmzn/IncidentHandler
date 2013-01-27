IncidentHandler
===============

Background: 

    So I initally starting building something to simply call or SMS me when there where issues in the office like the UPS
    losing its input feed or where core servers go down outside of normal operating hours. As I worked on that I fleshed 
    it out so that it would take a config with a list of users to notify initiall by SMS and if no-one responds to that to
    then begin calling those that are listed in the config.
    
    We don't have a follow-the-sun support environment so this was built out of a need to have an operational IT environment
    when the markets open at 7am in the morning but where there isn't a 24 hour team monitoring core services.
