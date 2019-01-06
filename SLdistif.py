# This lib contains functions which access and work with "disturbances" from Stockholm Lokaltrafik (SL)

# Import some libs
import sys
import config # The file containing the SL API and other stuff
import requests
import json

def getMainPathDisturbances(travelingPath):
    dist = getPathDisturbances(travelingPath)

    # Filter only "MainNews" into a new dict and the low prio to another dict
    MainDisturbances_dict = [x for x in dist if x['MainNews']==True]
    LowPrioDisturbances_dict = [x for x in dist if x['MainNews']==False]
  
    numberOfMainDisturbances = len(MainDisturbances_dict)
    numberOfLowPrioDisturbances = len(LowPrioDisturbances_dict)

    printout = False # Do something else with this. Separate print function or use as debug thingy only
    if printout == True:
        if numberOfMainDisturbances >= 1:
            print("High prio disturbances exists ("+str(numberOfMainDisturbances)+")")
            for disturbanceItem in MainDisturbances_dict:
                printKeyDistInfo(disturbanceItem)
        else:
            print("No High prio disturbances on the traveling path")

        if numberOfLowPrioDisturbances >= 1:
            print("Low prio disturbances exists ("+str(numberOfLowPrioDisturbances)+")")
            for disturbanceItem in LowPrioDisturbances_dict:
                printKeyDistInfo(disturbanceItem)
        else:
            print("No Low prio disturbances on the traveling path")

    # Return only the MainNews disturbances
    return MainDisturbances_dict


def getPathDisturbances(travelingPath):
    # Get the disturbances applicable to the specified traveling path
    lineNumber = getPathLines(travelingPath)
    transportMode = getPathTransportMode(travelingPath)
    dist = getDisturbances(transportMode, lineNumber)
    return dist

def getDisturbances(transportMode, lineNumber):
    # Get disturbances for the specied SL line(s) and transport mode
    # If transportMode or lineNumber is empty (""), they will treated as "ALL"
    # There are possibilities to be more specific for the disturbances to get
    # See https://www.trafiklab.se/node/12605/documentation
    #
    # http://api.sl.se/api2/deviations.<FORMAT>?key=<DIN API NYCKEL>&transportMode=<TRANSPORTMODE>
    # &lineNumber=<LINENUMBER>&siteId=<SITEID>&fromDate=<FROMDATE>&toDate=<TODATE>
    #
    # This is to be added if needed (new func of expanding this one)
    #
    req = createRequest(transportMode, lineNumber)
    r = requests.get(req)
    print(r.status_code)
    if(r.status_code == 200):
        #print ("All OK")
        issues = json.loads(r.text)["ResponseData"]
        return issues
    else:
        print ("Something went wrong. No answer from SL. Exiting")
        print ("Error messaage from SL: "+r.message)
        sys.exit(1)

def createRequest(transportMode, lineNumber):
    # Create the request to send towards the SL disturbance service end-point
    SLdistAPIkey = config.SLdistAPIkey # API-key to be added in config.py with one line "SLdistAPIkey = <YOUR-API-KEY>""
    req = 'http://api.sl.se/api2/deviations.Json?key='+SLdistAPIkey+'&transportMode='+transportMode+'&lineNumber='+lineNumber
    return req

def getPathLines(travelingPath):
    # Get train/bus/metro-lines for a path
    pathLineNumbersDict = {
        "Älvsjö-Kista": "41,42,42X,43",
        "Kista-Älvsjö": "41,42,42X,43",
        "Älvsjö-Kista-metro": "14,11",
        "Kista-Älvsjö-metro": "14,11"
    }
    if travelingPath in pathLineNumbersDict:
        return pathLineNumbersDict[travelingPath]
    else:
        print("No such traveling path defined, sorry")
        sys.exit(1)

def getPathTransportMode(travelingPath):
    # Get transport modes for a path
    pathTransportModeDict = {
        "Älvsjö-Kista": "train",
        "Kista-Älvsjö": "train",
        "Älvsjö-Kista-metro": "metro",
        "Kista-Älvsjö-metro": "metro"       
    }
    if travelingPath in pathTransportModeDict:
        return pathTransportModeDict[travelingPath]
    else:
        print("No such traveling path defined, sorry")
        sys.exit(1)
 
def printDistHeaders(disturbances):
    # If there are any disturbances, print header of the first one
    # Next, itterate over all disturbances / all important disturbances
    if disturbances[:]:
        for disturbanceItem in disturbances:
            print ("("+disturbanceItem['Updated']+') '+ disturbanceItem['ScopeElements']+":"+disturbanceItem['Header'])
    else:
        print("No disturbances! Celebrate")
    return

def printKeyDistInfo(disturbanceItem):
    print (disturbanceItem['ScopeElements']+":"+disturbanceItem['Header']+" ("+disturbanceItem['Updated']+') ')
    return





# ---- Not used ---- 
#
# Create function which can take the input parameters as optional arguments
# This instead of using positional arguments
# Perhaps we should move to this one instead?
# It become a bit more messy to call when building the function calls, but more future proof?
#def createRequest2(**options):
#    APIkey = config.SLdistAPIkey
#    
#    # If any of the optional arguments were given, apply them
#    if (options.get("transportMode") == "train" or options.get("transportMode") == "metro"):
#        print("you only care about the "+options.get("transportMode"))
#        transportMode = options.get("transportMode")
#    else:
#        print("all transports it is as you did not select any valid transportMode")
#        transportMode = ""
#
#    if options.get("lineNumber"):
#        print("you only care about the lines "+options.get("lineNumber"))
#        lineNumber = options.get("lineNumber")
#    elif not options.get("lineNumber"):
#        print("all lineNumbers it is as you did not select any valid lineNumber")
#        lineNumber = ""
#        
#    req = 'http://api.sl.se/api2/deviations.Json?key='+APIkey+'&transportMode='+transportMode+'&lineNumber='+lineNumber
#    return req
#
#
# Bonus info: If playing with importing modules to jupyter notebook, you can make sure your updates in the libs (.py) are reoaded by adding
# %load_ext autoreload
# %autoreload 2
# %reload_ext autoreload
# import SLdistif as sl