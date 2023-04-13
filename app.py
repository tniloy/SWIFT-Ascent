import json
import requests
from flask import app

# URL of the DSA Framework web service
dsa_input_url = "https://localhost:8000/getSimulatorInput"
dsa_feedback_url = "https://localhost:8000/submitSimulatorFeedback"
dsa_settings_url = "https://localhost:8000/updateSimulatorSettings"

# Define the initial simulator settings
simulator_settings = {"inclusion_zone_radius": 10, "base_station_count": 5}

# Define the headers for the API requests
headers = {'Content-type': 'application/json'}

# Define the initial simulator settings
counter = 0

while True:
    counter = counter+1
    if counter > 2:
        print("Exiting the loop.")
        break

    """
        Define the data to be sent as part of the initial API request
        Send a GET request to the DSA Framework web service
    """

    dsa_get_response = requests.get(dsa_input_url, verify=False)
    if dsa_get_response.status_code == 200:
        print("DSA data successfully fetched.")
        print(dsa_get_response.content)
    else:
        print("DSA data could not be fetched.")
        break
    # Print the response content
    # dsa_data_json = response.json()

    """
        Define the URL for the API
        Define the data to be sent as part of the API request
        Send a POST request to the API with the input data
    """

    simulator_api_url = "https://localhost:5000/parsesimulatordata"
    # simulator_api_data = dsa_data_json
    simulator_response = requests.post(simulator_api_url, data=json.dumps(dsa_get_response.json()), headers=headers, verify=False)

    if simulator_response.status_code == 200:
        print("DSA data submitted successfully to simulator.")
        print(simulator_response.content)
    else:
        print("DSA data could not be submitted successfully to simulator.")
        break
    # Get the response from the API
    # api_response = response.json()


    # Send feedback to the DSA
    # feedback_data = api_response
    feedback_response = requests.post(dsa_feedback_url, data=json.dumps(simulator_response.json()), headers=headers, verify=False)
    # feedback_response_json = feedback_response.json()
    # Check the response
    if feedback_response.status_code == 200:
        print("Feedback submitted successfully.")
        print(feedback_response.content)
    else:
        print("Failed to submit feedback to DSA.")
        break


    """
        Update the simulator settings
    """

    settings_response = requests.post(dsa_settings_url, data=json.dumps(simulator_settings), headers=headers, verify=False)
    # settings_response_json = settings_response.json()
    if settings_response.status_code == 200:
        print("Updated simulator settings with DSA successfully.")
        print(settings_response.content)
    else:
        print("Failed to update simulator settings with DSA.")
        break

if __name__ == '__main__':
    # Use a self-signed certificate for testing purposes
    context = ('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=6000, debug=True, ssl_context=context)

