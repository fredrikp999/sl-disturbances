# sl-disturbances
Trying out the SL REST API for disturbances
API-key needs to be added in config.py with one line "SLdistAPIkey = <YOUR-API-KEY>"
Retrieve the key from https://www.trafiklab.se
For more info on the API, check out: https://www.trafiklab.se/node/12605/documentation
\
To run in Docker:
docker build -t sldist . 
docker run -p 5000:5000 sldist 
  
To try it out, use these endpoints:
  http://localhost:5000/api/disturbances - returns json with the current disturbances on train route to work
  http://localhost:5000/api/startDistChecking - starts a loop which monitors disturbances and set lamp to RED/GREEN/BLUE
  http://localhost:5000/api/funny - bonus endpoint with some quotes
\
(The end-points and structure of what is returned will change to something more proper)
