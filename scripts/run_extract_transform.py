from os import path
import pandas as pd
from etl import extract_new, transform_new

# paths
archive_path = './archive'
zipcodes_path = './static/zipcode.csv'
stations_path = './static/stations.csv'

# zipcodes as list
zipcodes = pd.read_csv(zipcodes_path, usecols = [0]).iloc[:,0]

# stations as dict records
if path.exists(stations_path):
    stations = pd.read_csv(stations_path).to_dict(orient='records')

# run etl
extract_new(archive_path, zipcodes)
transform_new(archive_path, stations)
