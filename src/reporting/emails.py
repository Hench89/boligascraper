import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import pandas as pd
import numpy as np
import csv

def send_mail(send_from, send_to, subject, message, files=[],
    server="localhost", port=587, username='', password='',
    use_tls=True):

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for path in files:
        part = MIMEBase('application', "octet-stream")
        with open(path, 'rb') as file:
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment; filename="{}"'.format(Path(path).name))
        msg.attach(part)

    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

def get_latest(file_path: str, get_days: int):

    # load data and filter based on days
    df = pd.read_csv(file_path, quoting=csv.QUOTE_NONNUMERIC)
    df['market_days'] = np.int64(df['market_days'])
    df = df[df['market_days'] <= get_days].reset_index()

    # finetune column types
    df['zipcode'] = np.round(np.int64(df['zipcode']),0)
    df['list_price'] = np.round(np.int64(df['list_price']),0)
    df['market_days'] = np.round(np.int64(df['market_days']),0)

    # prepare some text
    txt = []
    for index in range(len(df)):
        zipcode = str(df.loc[index]['zipcode'])
        url = str(df.loc[index]['url'])
        price = str(df.loc[index]['list_price'])
        days = str(df.loc[index]['market_days'])
        txt.append(f'{str(index+1)}: ny bolig i {zipcode} på markedet i {days} dage til {price} kr. - se mere: {url}')

    s = "\r\n"
    s = s.join(txt)
    return s
