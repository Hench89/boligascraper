import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_ssl_mail(send_from, password, subject, body, server, port, send_to):

    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = ", ".join(send_to) if ';' in send_to else send_to

    part2 = MIMEText(body, 'html')
    msg.attach(part2)

    server = smtplib.SMTP_SSL('smtp.gmail.com', port)
    server.ehlo()
    server.login(send_from, password)
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()
    print('Email sent!')
