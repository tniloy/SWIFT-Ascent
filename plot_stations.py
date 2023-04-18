import gmplot
import os
import numpy as np


def plot_stations(lat_FSS, lon_FSS, base_stations):
    # gmap = gmplot.GoogleMapPlotter.from_geocode("USA", apikey="AIzaSyC4BI4H4SCVgA2nGASWUlGPpJS4f-jPjgw")
    center_lat = np.mean(lat_FSS)
    center_long = np.mean(lon_FSS)
    gmap = gmplot.GoogleMapPlotter(center_lat, center_long, 13, apikey="AIzaSyC4BI4H4SCVgA2nGASWUlGPpJS4f-jPjgw")


    gmap.marker(lat_FSS, lon_FSS, color='red')

    # Create the map

    # get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # specify the path to save the html file
    save_path = os.path.join(script_dir, "stations_map.html")

    for base in base_stations:
        gmap.marker(base['latitude'], base['longitude'], color='blue')
        gmap.circle(base['latitude'], base['longitude'], radius=0.38 * 1000, color='green')

    gmap.draw(save_path)


