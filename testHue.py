# This is just for trying out stuff before adding to the real program

from phue import Bridge
#from phue import Sensor
from datetime import datetime
import time

def tryHue():
	b = Bridge('192.168.0.82') # Move this out to config.py
	# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
	b.connect()
	# Get the bridge state (This returns the full dictionary that you can explore)
	b.get_api()
	lights = b.lights

	#for i in range(1,10):
	#	s = Sensor(b,i)
	#	print (i)
	#	print(s.state)
	#	print(s.name)
	#	print("---")

	#return b

	#s = b.get_sensor('Kitchen switch')
	#print(s)

	for i in range(1,50):
		s = b.get_sensor(i)
		#print("-------")
		# Print out only in there is a sensor on this position
		# If there is none, b.get_sensor will return an empty string
		if s:
			print (str(i)+": "+s['name'])

	# Sensor#30 is the motion sensor in the kitchen
	s = b.get_sensor(30)
	print(s)
	print("------")
	if (s['state']['status']==1):
		#Motion detected
		print("Someone is in the kitchen!")
	else:
		print("All quiet in the kitchen")

# Current sensors:
# 1: Daylight
# 2: Entrance switch
# 3: Dimmer Switch 2.companion
# 4: HomeAway
# 5: Samsung SM-G930F
# 6: Morgin i hallen
# 7: Living room switch
# 8: Dimmer Switch 7 SceneCycle
# 9: Kitchen switch
#
# For switches, you can use:
# lastupdated - to see when last pressed
# buttonevent - for what was the last press, where 1002 = "On"/1 and 4002 = "Off"/0

def main():
	# Get bridge state and full dictonary
	b = tryHue()

if __name__== "__main__":
  main()