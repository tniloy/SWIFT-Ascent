import json
import requests
from flask import app

# URL of the DSA Framework web service
dsa_input_url = "https://localhost:8000/getSimulatorInput"
# values expected from DSA
#   "lat_FSS":37.20250,
#   "lon_FSS":-80.43444,
#   "radius": 5000,
#   "simulation_count" : 3,
#   "bs_ue_max_radius": 1000,
#   "bs_ue_min_radius": 1,
#   "base_station_count": 33
dsa_feedback_url = "https://localhost:8000/submitSimulatorFeedback"
dsa_settings_url = "https://localhost:8000/updateSimulatorSettings"

# Define the headers for the API requests
headers = {'Content-type': 'application/json'}

# Define the data to be sent as part of the initial API request
input_data = {}
response = requests.get(dsa_input_url, data=json.dumps(input_data), headers=headers, verify=False)
dsa_data_json = response.json()

# Define the initial simulator settings
simulator_settings = {"inclusion_zone_radius": 10, "base_station_count": 5}

while True:
    # Define the URL for the API
    simulator_api_url = "https://localhost:5000/parsesimulatordata"

    # Define the data to be sent as part of the API request
    simulator_api_data = dsa_data_json

    # Send a POST request to the API with the input data
    response = requests.post(simulator_api_url, data=json.dumps(simulator_api_data), headers=headers, verify=False)

    # Get the response from the API
    api_response = response.json()

    # Send feedback to the DSA
    feedback_data = {"feedback": api_response}
    feedback_response = requests.post(dsa_feedback_url, data=json.dumps(feedback_data), headers=headers, verify=False)
    feedback_response_json = feedback_response.json()
    if feedback_response_json["status"] == "failure":
        print("Failed to submit feedback to DSA")
        break

    # Update the simulator settings
    settings_response = requests.post(dsa_settings_url, data=json.dumps(simulator_settings), headers=headers, verify=False)
    settings_response_json = settings_response.json()
    if settings_response_json["status"] == "failure":
        print("Failed to update simulator settings with DSA")
        break

    # Get the new input data from the DSA
    response = requests.get(dsa_input_url, data=json.dumps(input_data), headers=headers, verify=False)
    dsa_data_json = response.json()

if __name__ == '__main__':
    # Use a self-signed certificate for testing purposes
    context = ('cert.pem', 'key.pem')
    # context = ('/Users/ani/Desktop/Projects/Projects2/SWIFT-Ascent/cert.pem', '/Users/ani/Desktop/Projects/Projects2/SWIFT-Ascent/key.pem')
    app.run(host='0.0.0.0', port=6000, debug=True, ssl_context=context)