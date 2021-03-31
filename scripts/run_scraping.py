import csv
import os
from composer import wrap_compose


# compute
archive_path = './output/boliga.csv'
zipcodes_path = './static/zipcode.csv'
stations_path = './static/stations.csv'
df = wrap_compose(zipcodes_path, stations_path, archive_path)

# save archive
if not os.path.exists(os.path.dirname(archive_path)):
    try:
        os.makedirs(os.path.dirname(archive_path))
    except Exception:
        raise

df.to_csv(archive_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
print('Archive stored!')