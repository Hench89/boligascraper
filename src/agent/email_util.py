import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pretty_html_table import build_table
from urllib.parse import urlparse


def get_html_df(df, df_title):
    url_columns = [c for c in df.columns if 'url' in c]
    df['links'] = df.apply(lambda x: ', '.join([add_url_tags(x[c]) for c in url_columns]), axis=1)
    df = df.drop(columns=url_columns)
    def trunc(txt):
        return txt[:15] + '..' if len(txt) > 15 else txt
    df['address'] = df.apply(lambda x: trunc(x.address), axis=1)

    theme = 'red_dark'
    html_table = build_table(df, color=theme, font_size='small')
    html_table = html_table.replace("URLSTART", "<a href=\"")
    html_table = html_table.replace("URLMID", "\">")
    html_table = html_table.replace("URLEND", "</a>")
    title_txt = f'<b>{df_title}</b><br>'
    return title_txt + html_table


def add_url_tags(url):
    if url == '-' or url == '':
        return url
    domain = get_domain(url)
    return "URLSTART" + url + "URLMID" + domain + "URLEND"


def get_domain(url):
    domain = urlparse(url).netloc
    domain = domain.replace('.dk', '')
    domain = domain.replace('.com', '')
    domain = domain.replace('.', '')
    domain = domain.replace('www', '')
    domain = domain.replace('google', 'maps')
    return domain


def send_email(email_body):

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


def send_ssl_mail(send_from, password, subject, body, server, port, send_to):

    # construct part1
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ", ".join(send_to) if type(send_to) == list else send_to

    # construct part2
    part2 = MIMEText(body, 'html')
    msg.attach(part2)

    # connect and send email
    server = smtplib.SMTP_SSL('smtp.gmail.com', port)
    server.ehlo()
    server.login(send_from, password)
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()
    print('Email sent!')
