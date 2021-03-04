from reporting.emails import send_ssl_mail, get_email_body
import os

send_from = os.getenv('MY_MAILFROM')
send_to = os.getenv('MY_MAILTO').split(";")
password = os.getenv('MY_MAILPASS')
server = "smtp.gmail.com"
port = 465

subject = "Boliga Listings"
archive_file_path = "./output/boliga.csv"
body = get_email_body(archive_file_path, 1)

#print(message)
send_ssl_mail(send_from, password, subject, body, server, port, send_to)
