from datetime import datetime
import SLdistif as sl
import time
import reactOnSL as rsl
from tinydb import TinyDB, Query
import json
import pprint

def main():
	# Get bridge state and full dictonary
	b = rsl.setupHue()

	for n in range (1,100000):
		kitchenMovement = rsl.checkKitchenMotion(b)
		#if kitchenMovement == True:
		if 1==1: ## Just for testing, triger even if no movement in the kitchen
			print ("Ok, time to start checking for disturbances on SL - if that is enabled")
			enabledsetting = isSLdistCheckEnabled()
			print ("Enabled?:"+enabledsetting)
			if enabledsetting == "True":
				rsl.kickOffLoop(b)
		# Wait some time before checking again
		time.sleep(10)

def isSLdistCheckEnabled():
		# Query the database to see if the "interrest" "SLdist" is enabled or not
		# An array of records is returned. We expect it to only one and if not we pretend so...
		TheQuery = Query()
		enabledsetting = db.search(TheQuery.name == 'SLdist')[0]
		print (json.dumps(enabledsetting, indent=2, sort_keys=True))
		enabled = enabledsetting["enabled"]
		return enabled

db = TinyDB('db2.json')

if __name__ == "__main__":
	main()