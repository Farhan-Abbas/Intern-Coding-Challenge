'''
Strategy: To identify the common signals between the two sensor data, we will need to compare the latitude and longitude of each signal
in the first sensor data with the latitude and longitude of each signal in the second sensor data.
If the distance between two signals is less than 100 meters, then we will consider these two signals to be the same signal.
Since the points use the WGS84 format, To calculate the distance between two lat/lon points, we will use the Haversine formula.
'''

import pandas as pd # we will use the pandas library to load data from the csv and json files.
import math # used to calculate the distance between two lat/lon points.
import json # used to save the output in a json file.

# convert angle in degrees to radians
def deg2rad(deg):
    return deg * (math.pi / 180)

# function to calculate the distance between two lat/lon points in meters.
# since the points use the WGS84 format, we will use the Haversine formula to calculate the distance.
# source of this formula: https://www.movable-type.co.uk/scripts/latlong.html
def get_distance_btw_two_lat_lon_points(lat1, lon1, lat2, lon2):
    radius_of_earth = 6378137 # Radius of the earth in meters using the WGS84 ellipsoid.
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius_of_earth * c # Distance in meters
    return d    

# good practice to handle exceptions when loading data from files.
try:
    sensor_data_one = pd.read_csv('SensorData1.csv') # load the first sensor data from the csv file.
    sensor_data_two = pd.read_json('SensorData2.json') # load the second sensor data from the json file.
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)
except pd.errors.EmptyDataError as e:
    print(f"Error: {e}")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Error: {e}")
    exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit(1)

common_signals = {} # dictionary to store the common signals between the two sensor data.

# loop through the two sensor data to find the common signals. calculate the distance between each pair of points.
# if the distance is less than 100 meters, then the two points are considered to be the same signal.
# we then store the common signals in the common_signals dictionary.
for i in range(len(sensor_data_one)):
    for j in range(len(sensor_data_two)):
        try:
            lat1 = sensor_data_one['latitude'][i]
            lon1 = sensor_data_one['longitude'][i]
            lat2 = sensor_data_two['latitude'][j]
            lon2 = sensor_data_two['longitude'][j]

            distance_between_points = get_distance_btw_two_lat_lon_points(lat1, lon1, lat2, lon2)
            if distance_between_points < 100:
                if sensor_data_one['id'][i] not in common_signals:
                    common_signals[int(sensor_data_one['id'][i])] = int(sensor_data_two['id'][j])
                else:
                    # if the signal from sensor one is already in the dictionary, then we will add the new signal from sensor two in addition to the previous sensor two signal.
                    # there is no specification on how to handle this case so I assumed that if there is a signal in sensor one data that is less than 100 meters from
                    # two signals in the sensor two data, then we will store both of these two signals in the list.
                    common_signals[int(sensor_data_one['id'][i])].append(int(sensor_data_two['id'][j]))
                break
        except KeyError as e:
            print(f"KeyError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# save the common signals in a json file.
try:
    with open('Output.json', 'w') as f:
        json.dump(common_signals, f)
except IOError as e:
    print(f"Error writing to file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
