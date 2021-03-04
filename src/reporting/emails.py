import pandas as pd
import numpy as np
import csv
import smtplib
from email.mime.text import MIMEText

def send_ssl_mail(send_from, password, subject, body, server, port, send_to):

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ", ".join(send_to)

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
