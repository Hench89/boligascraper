from .html import get_html_df
from .emails import send_ssl_mail
import pandas as pd
import os

def compose(root_path):

    print(f'===== MAILING REPORT =====')

    # fetch for sale data
    for_sale_report_path = f'{root_path}/report/for_sale_report.json'
    df = pd.read_json(for_sale_report_path, orient='table')
    for_sale_email_body = get_html_df(df, 'For Sale')

    # fetch sold data
    for_sale_report_path = f'{root_path}/report/sold_report.json'
    df = pd.read_json(for_sale_report_path, orient='table')
    sold_email_body = get_html_df(df, 'Sold')

    email_body = '<br><br>'.join([for_sale_email_body, sold_email_body])

    # retrieve environment variables
    try:
        env_send_from = os.getenv('MAILFROM')
        env_send_to = os.getenv('MAILTO')
        env_send_to = env_send_to.split(';') if ';' in env_send_to else env_send_to
        env_password = os.getenv('MAILPASSWORD')
    except:
        print('Unable to retrieve environment variables!')
        pass

    # send email
    send_ssl_mail(
        send_from = env_send_from,
        password = env_password,
        subject = "Housing Agent",
        body = email_body,
        server = "smtp.gmail.com",
        port = 465,
        send_to = env_send_to
    )
