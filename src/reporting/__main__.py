from reporting.emails import send_mail, get_latest
import os


send_from = os.getenv('MY_MAILTO')
send_to = [os.getenv('MY_MAILFROM')]
password = os.getenv('MY_MAILPASS')
message = get_latest("./output/boliga.csv", 1)
server = "smtp.gmail.com"
subject = "Boliga Listings"
files = ["./output/boliga.csv"]

#print(message)
send_mail(send_from, send_to, subject, message, files, server, port=587, username=send_from, password=password,use_tls=True)
