from reporting.emails import send_ssl_mail
from dfutils.html import get_html_df
import os
import sys
import traceback
import pandas as pd
import csv

# retrieve environment variables
try:
    env_send_from = os.getenv('MAILFROM')
    env_send_to = os.getenv('MAILTO')
    env_send_to = env_send_to.split(';') if ';' in env_send_to else env_send_to
    env_password = os.getenv('MAILPASSWORD')
except:
    print('Unable to retrieve environment variables')
    traceback.print_exc()
    sys.exit()

# prepare table
try:

    # read archive
    archive_file_path = "./output/boliga.csv"
    dtype_schema = {'list_price': int, 'living_area': int, 'rooms': int, 'market_days' : int}
    df = pd.read_csv(archive_file_path, quoting=csv.QUOTE_NONNUMERIC, dtype=dtype_schema)

    # prepare archive for email
    output_columns = ['address', 'property_type', 'list_price', 'living_area', 'rooms', 'url', 'gmaps', 'station_dist_km', 'market_days']
    df = df[output_columns]
    df = df[df['market_days'] <= 4].reset_index()
    df['list_price'] = df.apply(lambda x: '{:,}'.format(x.list_price).replace(',', '.'), axis=1)

    # get html table
    link_columns = ['url', 'gmaps']
    email_body = get_html_df(df, link_columns=link_columns)

except:
    print('Unable to read and prepare table from archive')
    traceback.print_exc()
    sys.exit()

# send email
try:
    send_ssl_mail(
        send_from = env_send_from,
        password = env_password,
        subject = "Boliga Listings",
        body = email_body,
        server = "smtp.gmail.com",
        port = 465,
        send_to = env_send_to
    )
except:
    traceback.print_exc()
    sys.exit()
