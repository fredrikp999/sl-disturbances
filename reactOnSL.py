#!/usr/bin/python3
# This is the main program
# Intended to run in a loop during the time there is an interest of soon traveling
# e.g. in the morning before going to work
# If there are any high priority disturbances on the travel path (e.g. to work), 
# a lamp will turn RED. If there is not but there are unusually many low prio issues, lamp will turn BLUE
# If all are OK (no high prio and not that many low prio), then turn lamp GREEN 
#
# To decide how this is to be triggered and where scheduling shall be handled. E.g. no use to mess with lamp if no-one home etc.
# One way could be to wait for Philips Hue motion sensor going off in the morning before starting up

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
	kickOffLoop(b)

	# Get a dictionary with the light name as the key
	#light_names = b.get_light_objects('name')
	#print(light_names)

def kickOffLoop(b):
	# Get a dictionary with the light name as the key
	light_names = b.get_light_objects('name')

	# Loop for 50 minutes (10 times, check every five minutes)
	for x in range(10):
		# Get the current disturbances on the specified travelling path
		dist = sl.getPathDisturbances("Älvsjö-Kista")
		# Print the disturbances out
		print("--------------")
		print(datetime.now().time())
		sl.printDistHeaders(dist)
		# Split out the high vs low prio disturbances and count them
		MainDisturbances_dict = [x for x in dist if x['MainNews']==True]
		LowPrioDisturbances_dict = [x for x in dist if x['MainNews']==False]
		numberOfMainDisturbances = len(MainDisturbances_dict)
		numberOfLowPrioDisturbances = len(LowPrioDisturbances_dict)
		

		# IF there are at least one high prio disturbance, turn RED
		if (numberOfMainDisturbances >=1):
			print("High prio disturbances ("+str(numberOfMainDisturbances)+"), please check!")
			light_names["Sektetär"].on = True
			light_names["Sektetär"].brightness = 254
			light_names["Sektetär"].hue = 65535 # RED
			# Here also add some more notification e.g. play sound on Sonos and/or
			# push info on the disturbance to the mobile / google home screen etc.

		# else if there are quite some low prio disturbances, turn BLUE
		elif (numberOfLowPrioDisturbances > 10):
			print("Many LowPrio disturbances ("+str(numberOfLowPrioDisturbances)+"), better check")
			light_names["Sektetär"].on = True
			light_names["Sektetär"].brightness = 254
			light_names["Sektetär"].hue = 46920 #BLUE

		# and if no high prio and only low number of low prio, tyrn GREEN
		elif (numberOfLowPrioDisturbances <= 10):
			print("Just a few LowPrio disturbances ("+str(numberOfLowPrioDisturbances)+"), you can relax")
			light_names["Sektetär"].on = True
			light_names["Sektetär"].brightness = 150
			light_names["Sektetär"].hue = 25500 # GREEN
		print("+++++++++++++++")
		# Sleep for 5 minutes
		time.sleep(5*60)
  
if __name__== "__main__":
  main()
