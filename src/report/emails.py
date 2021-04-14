import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
