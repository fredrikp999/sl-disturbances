# This is the app for running this as a service with a REST API
# Using flask
# Authentication token for Hue Bridge needs to be fixed
# Right now you need to approve connetion every time you rebuild the docker-file / restart the web-server
#
# Put example: curl http://localhost:5000/api/v1/paras/checkSL -d "data=False" -X PUT
# GET example: curl http://localhost:5000/api/v1/paras/checkSL
#
# /api/v1/journeys/journey - id,title,lines,type
# /api/v1/journeys/journey/limits/highlimit - 
# /api/v1/indicators/indicator - id,type,reference,enabled
# /api/v1/indicators/indicator/ 
# /api/v1/actions/action - journey, indicator, enabled
# /api/v1/interrests/interrest/sldist - enabled (True/False)

from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
import random
from phue import Bridge
from datetime import datetime
import SLdistif as sl
import time
import reactOnSL as rsl
from tinydb import TinyDB, Query

from quotes import funny_quotes


# ParaList
# shows a list of all parameters
class ParaList(Resource):
	def get(self):
		return PARAS

class DisturbanceList(Resource):
	def get(self):
		dist = sl.getPathDisturbances("Älvsjö-Kista")
		return jsonify(dist)

class InterrestSLdist(Resource):
	# curl http://localhost:5000/api/v1/interrests/sldist
	def get(self):
		TheQuery = Query()
		enabledsetting = db.search(TheQuery.name == 'SLdist')
		return jsonify(enabledsetting)

	def put(self):
		# curl http://localhost:5000/api/v1/interrests/sldist -d "data=False" -X PUT
		# curl http://localhost:5000/api/v1/interrests/sldist -d "data=True" -X PUT
		TheQuery = Query()
		args = parser.parse_args()
		enabledsetting = {'enabled': args['data']}		
		db.update(enabledsetting, TheQuery.name == 'SLdist')
		return jsonify(enabledsetting)

class Initialize(Resource):
	# Clean database and add in default values
	# This end-point is not a goot RESTful endpoint, but good for now until better name...
	# curl http://localhost:5000/api/v1/initialize -d "data=yespleaseresethedatabase" -X PUT
	def get(self):
		return jsonify({'heyhey':'hoho'})

	def put(self):
		args = parser.parse_args()
		if args['data'] == "yespleaseresethedatabase":
			db.purge()
			db.insert({'type':'interrest', 'name':'SLdist', 'enabled':"False"})
			db.insert({'type':'interrest', 'name':'anotherone', 'enabled':"False"})
			return jsonify({'did it go ok':'yes, I did initialize the db'})
		else: 
			return jsonify({'sorry, please provide the magic word...':'yespleaseresethedatabase'})

# shows a single parameter and lets you update it
class Para(Resource):
	def get(self, para_id):
		if para_id in PARAS:
			return PARAS[para_id]
		else:
			abort_if_para_doesnt_exist(para_id)

	def put(self, para_id):
		args = parser.parse_args()
		para = {'value': args['data']}
		PARAS[para_id] = para
		#db.insert(para)
		db.update
		return para, 201

def abort_if_para_doesnt_exist(para_id):
	abort(404, message="Parameter {} doesn't exist".format(para_id))

PARAS = {
	"checkSL": {'value': 'False'},
	"TravelingPath": {'value': 'Älvsjö-Kista'}
}

parser = reqparse.RequestParser()
parser.add_argument('data')
app = Flask(__name__)
api = Api(app)
db = TinyDB('db2.json')

##
## Actually setup the Api resource routing here
##
api.add_resource(ParaList, '/api/v1/paras')
api.add_resource(Para, '/api/v1/paras/<string:para_id>')
api.add_resource(DisturbanceList, '/api/v1/disturbances')
api.add_resource(InterrestSLdist, '/api/v1/interrests/sldist')
api.add_resource(Initialize, '/api/v1/initialize')

"""
# This is the vanilla flask way of creating RESTful API
# Skipping this and using flask_restful instead - see above
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
"""

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)