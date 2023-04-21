import gmplot
import os
import numpy as np
import math


def plot_stations(lat_FSS, lon_FSS, base_stations, inr_each_bs):
    # gmap = gmplot.GoogleMapPlotter.from_geocode("USA", apikey="AIzaSyC4BI4H4SCVgA2nGASWUlGPpJS4f-jPjgw")
    center_lat = np.mean(lat_FSS)
    center_long = np.mean(lon_FSS)
    gmap = gmplot.GoogleMapPlotter(center_lat, center_long, 13, apikey="AIzaSyC4BI4H4SCVgA2nGASWUlGPpJS4f-jPjgw")
    buckets = 5
    # https://coolors.co/palette/03071e-370617-6a040f-9d0208-d00000-dc2f02-e85d04-f48c06-faa307-ffba08
    color_palette = ['#FFBA08', '#F48C06', '#DC2F02', '#9D0208', '#370617']
    min_inr_each_bs, max_inr_each_bs = min(inr_each_bs), max(inr_each_bs)
    bucket_size = (max_inr_each_bs - min_inr_each_bs)/buckets

    gmap.marker(lat_FSS, lon_FSS, color='gold', title='FSS Receiver', label='F')

    # Create the map

    # get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # specify the path to save the html file
    save_path = os.path.join(script_dir, "stations_map.html")

    for idx, base in enumerate(base_stations):
        bucket_match = int(math.ceil(inr_each_bs[idx]-min_inr_each_bs)/bucket_size)
        if base['status'] == 1:
            gmap.marker(base['latitude'], base['longitude'], color='green', title=f"BS | INR: {round(inr_each_bs[idx], 2)}, Status: Active", label='B')
            print(bucket_match, bucket_match % buckets)
            gmap.circle(base['latitude'], base['longitude'], radius=inr_each_bs[idx]*15, color=color_palette[bucket_match % buckets])
            # gmap.scatter(base['latitude'], base['longitude'], color=color_palette[bucket_match % buckets], colorbar=True)
            # gmap.text(37.793575, -122.464334, 'Presidio')
            # gmap.text(37.766942, -122.441472, 'Buena Vista Park', color='blue')
        else:
            gmap.marker(base['latitude'], base['longitude'], color='red', title="Status: Inactive", label='B')
            # gmap.circle(base['latitude'], base['longitude'], radius=inr_each_bs[idx], color='green')

    gmap.draw(save_path)


