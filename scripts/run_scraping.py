import csv
import os
from scraper.reader import compute


# compute
archive_path = './output/boliga.csv'
zipcodes_path = './static/zipcode.csv'
stations_path = './static/stations.csv'
df = compute(archive_path, zipcodes_path, stations_path)

# save archive
print('Storing to archive')

if not os.path.exists(os.path.dirname(archive_path)):
    try:
        os.makedirs(os.path.dirname(archive_path))
    except OSError:
        raise

df.to_csv(archive_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
