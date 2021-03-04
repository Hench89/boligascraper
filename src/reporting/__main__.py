from reporting.emails import send_ssl_mail, get_email_body
import os

send_from = os.getenv('MAILFROM')
send_to = os.getenv('MAILTO').split(";")
password = os.getenv('MAILPASSWORD')
server = "smtp.gmail.com"
port = 465

subject = "Boliga Listings"
archive_file_path = "./output/boliga.csv"
body = get_email_body(archive_file_path, 1)

#print(body)
send_ssl_mail(send_from, password, subject, body, server, port, send_to)
