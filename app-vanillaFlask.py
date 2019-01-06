# This is the app for running this as a service with a REST API
# Using flask
# Authentication token for Hue Bridge needs to be fixed
# Right now you need to approve connetion every time you rebuild the docker-file / restart the web-server

from flask import Flask, jsonify
import random
from phue import Bridge
from datetime import datetime
import SLdistif as sl
import time
import reactOnSL as rsl

from quotes import funny_quotes

app = Flask(__name__)


@app.route("/api/disturbances")
def serve_disturbances():
	dist = sl.getPathDisturbances("Älvsjö-Kista")
	return jsonify(dist)

@app.route("/api/startDistChecking")
# Really ugly way of doing this, but done as a start to show loop can be triggered
# Todo: Separate the start/stop from the actual "loop"
# This make it possible to return a response to the start request
# and end that session. Now it just hangs and is ugly...
def serve_startDistChecking():
	# Set up Philips Hue connection
	# and return a handle
	b = rsl.setupHue()
	# Start up a loop which checks disturbances on sl path to work
	# Keep it running for one hour or so
	print ("Starting checking disturbances")
	rsl.kickOffLoop(b)
	return ("Done. SL disturbances checked for some time...")

@app.route("/api/funny")
def serve_funny_qotes():
	quotes = funny_quotes()
	no_of_quotes = len(quotes)
	selected_quote = quotes[random.randint(0, no_of_quotes -1)]
	return jsonify(selected_quote)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)