import json

import requests
from flask import app

# URL of the DSA Framework web service
dsa_url = "https://127.0.0.1:8001/getSimulatorInput"
# values expected from DSA
#   "lat_FSS":37.20250,
#   "lon_FSS":-80.43444,
#   "radius": 5000,
#   "simulation_count" : 3,
#   "bs_ue_max_radius": 1000,
#   "bs_ue_min_radius": 1,
#   "base_station_count": 33

# Send a GET request to the DSA Framework web service
response = requests.get(dsa_url, verify=False)

# Print the response content
print(response.content)

# Get the response data in JSON format
dsa_data_json = response.json()

# Define the URL for the API
simulator_api_url = "https://127.0.0.1:5000/parsesimulatordata"

# Define the headers for the API request
headers = {'Content-type': 'application/json'}

# Define the data to be sent as part of the API request
simulator_api_data = dsa_data_json

# Send a POST request to the API with the output data
response = requests.post(simulator_api_url, data=json.dumps(simulator_api_data), headers=headers, verify=False)

# Get the response from the API
api_response = response.json()

# Print the API response
print(api_response)

# if __name__ == '__main__':
#     # Use a self-signed certificate for testing purposes
#
#     context = ('./cert.pem', './key.pem') # Use Absolute Paths locally if Relative ones not working
#     app.run(host='0.0.0.0',
#         port=6000,
#         debug=True, ssl_context=context)