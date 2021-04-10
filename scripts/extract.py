import pandas as pd
from etl import extract_sold, extract_estate

# zipcodes as list
zipcodes_path = './static/zipcode.csv'
zipcodes = pd.read_csv(zipcodes_path, usecols = [0]).iloc[:,0]

# extract batch of sold data
archive_path = './archive'
#extract_sold(archive_path, zipcodes)

# update sold entries
archive_path = './archive'
extract_estate(archive_path, zipcodes)
