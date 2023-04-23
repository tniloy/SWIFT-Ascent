"""
Swift Ascent Master Control REST API Server for CCI-SWIFT ASCENT

Created: Jan 29, 2023
Author/s: Rishabh Rastogi(rrishabh@vt.edu)
Advised by Dr. Eric Burger (ewburger@vt.edu) and Dr. Vijay K Shah (vshah22@gmu.edu)
For SWIFT-ASCENT
"""

import json
import requests

# from Simulator import app
from plot_stations import plot_stations
from show_graph import plot_graph
import webbrowser
import os
import warnings

warnings.filterwarnings("ignore")

# URL of the DSA Framework web service
dsa_input_url = "https://localhost:8000/getSimulatorInput"
simulator_api_url = "https://localhost:5000/parsesimulatordata"
dsa_feedback_url = "https://localhost:8000/submitSimulatorFeedback"
dsa_settings_url = "https://localhost:8000/updateSimulatorSettings"

# Define the headers for the API requests
headers = {'Content-type': 'application/json'}

# Define the initial simulator settings
counter = 0

while True:
    counter = counter + 1
    if counter > 3:
        print("Exiting the loop.\n")
        break

    if counter == 1:
        rain = False
    else:
        rain = True

    """
        Define the data to be sent as part of the initial API request
        Send a GET request to the DSA Framework web service
    """

    print("\n\nSWIFT ASCENT Run {}\n".format(counter))
    dsa_get_response = requests.get(dsa_input_url, verify=False)
    if dsa_get_response.status_code == 200:
        print("DSA data successfully fetched.")
        radius = dsa_get_response.json()['radius']
        bs_ue_max_radius = dsa_get_response.json()['bs_ue_max_radius']
        exclusion_zone_radius = dsa_get_response.json()['exclusion_zone_radius']
        rain_rate = dsa_get_response.json()['rain_rate']
        print("Context from DSA: Weather Context: {}, FSS radius={}, base station max radius: {}".format("Rainy, with rain rate of {} mm/hr".format(rain_rate) if rain else "Sunny", radius, bs_ue_max_radius))
    else:
        print("DSA data could not be fetched.")
        break

    # Extract the FSS and base station data from the API response
    lat_FSS = dsa_get_response.json()['lat_FSS']
    lon_FSS = dsa_get_response.json()['lon_FSS']
    base_stations = dsa_get_response.json()['base_stations']


    # temporary code begin

    json_obj = json.loads(dsa_get_response.text)

    # Modify the value of the "rain" key
    json_obj['rain'] = rain

    # Convert the modified JSON object back to a string
    dsa_get_response = json.dumps(json_obj)

    # temporary code begin

    """
        Define the URL for the API
        Define the data to be sent as part of the API request
        Send a POST request to the API with the input data
    """

    # simulator_api_data = dsa_data_json
    print("Trying to feed data from DSA in Simulator....")
    simulator_response = requests.post(simulator_api_url, data=dsa_get_response, headers=headers, verify=False)
    html_image = ""

    if simulator_response.status_code == 200:
        print("DSA data submitted successfully to simulator.")
        # print(simulator_response.content)
        html_image = simulator_response.json()['html_Interference_Noise']
    else:
        print("DSA data could not be submitted successfully to simulator.")
        break

    # Plot the stations on a map
    print("Plotting output from Simulator...")
    plot_stations(lat_FSS, lon_FSS, rain, base_stations, simulator_response.json()['Interference_values_UMi_each_Bs'])
    # Plot the graph on a map
    plot_graph(html_image)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = "Results.html"
    save_path = os.path.join(script_dir, html_file_path)
    # Open the file in the default web browser
    webbrowser.open('file://' + save_path)

    # Send feedback to the DSA
    feedback_response = requests.post(dsa_feedback_url, data=json.dumps(simulator_response.json()), headers=headers, verify=False)
    # Check the response
    if feedback_response.status_code == 200:
        print("Feedback from Simulator submitted successfully back to DSA.")
        print("Output for run no. {} of Swift Framework: {}".format(counter, feedback_response.json()['message']))
    else:
        print("Failed to submit feedback to DSA.")
        break


# if __name__ == '__main__':
#     # Use a self-signed certificate for testing purposes
#     context = ('cert.pem', 'key.pem')
#     app.run(host='0.0.0.0', port=6000, debug=True, ssl_context=context)

