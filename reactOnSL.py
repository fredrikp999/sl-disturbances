#!/usr/bin/python
# This is the main program
# Intended to run in a loop during the time there is an interest of soon traveling
# e.g. in the morning before going to work
# If there are any high priority disturbances on the travel path (e.g. to work), 
# a lamp will turn RED. If there is not but there are unusually many low prio issues, lamp will turn yellow
# If all are OK (no high prio and not that many low prio), then turn lamp GREEN 
# To decide how this is to be run and where scheduling shall be handled. E.g. no use to mess with lamp if no-one home etc.


from phue import Bridge
from datetime import datetime
import SLdistif as sl
import time

def setupHue():
	b = Bridge('192.168.0.82') # Move this out to config.py
	# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
	b.connect()
	# Get the bridge state (This returns the full dictionary that you can explore)
	b.get_api()
	lights = b.lights
	return b

def main():
	# Get bridge state and full dictonary
	b = setupHue()
	# Get a dictionary with the light name as the key
	light_names = b.get_light_objects('name')

	for x in range(10):
		dist = sl.getPathDisturbances("Älvsjö-Kista")
		sl.printDistHeaders(dist)
		MainDisturbances_dict = [x for x in dist if x['MainNews']==True]
		LowPrioDisturbances_dict = [x for x in dist if x['MainNews']==False]
		numberOfMainDisturbances = len(MainDisturbances_dict)
		numberOfLowPrioDisturbances = len(LowPrioDisturbances_dict)
		
		print(datetime.now().time())
		if (numberOfLowPrioDisturbances > 4):
			print("Many LowPrio disturbances, ("+str(numberOfLowPrioDisturbances)+"), better check")
			light_names["Sektetär"].on = True
			light_names["Sektetär"].brightness = 254
			light_names["Sektetär"].hue = 15000
		elif (numberOfLowPrioDisturbances <= 4):
			print("Just a few LowPrio disturbances ("+str(numberOfLowPrioDisturbances)+"), just relax")
			light_names["Sektetär"].on = True
			light_names["Sektetär"].brightness = 150
			light_names["Sektetär"].hue = 5000

		time.sleep(60)
  
if __name__== "__main__":
  main()



