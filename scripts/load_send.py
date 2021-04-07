from utils import send_ssl_mail
from etl import get_html_dataframe
import os
import sys
import traceback

# retrieve environment variables
try:
    env_send_from = os.getenv('MAILFROM')
    env_send_to = os.getenv('MAILTO')
    env_send_to = env_send_to.split(';') if ';' in env_send_to else env_send_to
    env_password = os.getenv('MAILPASSWORD')
except:
    print('Unable to retrieve environment variables!')
    traceback.print_exc()
    sys.exit()

# prepare table
try:

    # read archive
    archive_path = "./archive/"
    df = get_html_dataframe(archive_path)

except:
    print('Unable to read and prepare table from archive!')
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
