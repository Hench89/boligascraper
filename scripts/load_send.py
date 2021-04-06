from utils import get_html_df, send_ssl_mail
import os
import sys
import traceback
from etl import load

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
    archive_path = "./archive/"
    df = load(archive_path)

    # prepare archive for email
    output_columns = ['address', 'property_type', 'list_price', 'living_area', 'rooms', 'url', 'gmaps', 'station_dist_km', 'market_days']
    link_columns = ['url', 'gmaps']
    
    # get table for villa
    df['list_price'] = df.apply(lambda x: '{:,}'.format(x.list_price).replace(',', '.'), axis=1)
    df = df[output_columns]
    df = df[df['market_days'] <= 7].reset_index()
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
