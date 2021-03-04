import pandas as pd
import numpy as np
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table

def send_ssl_mail(send_from, password, subject, body, server, port, send_to):

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ", ".join(send_to)

    part2 = MIMEText(body, 'html')
    msg.attach(part2)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', port)
        server.ehlo()
        server.login(send_from, password)
        server.sendmail(send_from, send_to, msg.as_string())
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')


def get_email_body(file_path: str, get_days: int):

    # load data and filter based on days
    df = pd.read_csv(file_path, quoting=csv.QUOTE_NONNUMERIC)
    df['market_days'] = np.int64(df['market_days'])
    df = df[df['market_days'] <= get_days].reset_index()

    # finetune column types
    df['index'] = df.index +1
    df['list_price'] = np.round(np.int64(df['list_price']),0)
    df['living_area'] = np.round(np.int64(df['living_area']),0)
    df['rooms'] = np.round(np.int64(df['rooms']),0)
    df['market_days'] = np.round(np.int64(df['market_days']),0)
    df['url'] = "LINKSTART" + df['url'] + "LINKEND"

    # put together
    output_columns = ['index', 'address1', 'address2', 'list_price', 'living_area', 'rooms', 'url', 'market_days']
    html_table_blue_light = build_table(df[output_columns], 'red_dark')
    html_table_blue_light = html_table_blue_light.replace("LINKSTART", "<a href=\"")
    html_table_blue_light = html_table_blue_light.replace("LINKEND", "\">LINK</a>")

    return html_table_blue_light
