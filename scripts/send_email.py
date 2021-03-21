from reporting.emails import send_ssl_mail, get_email_body
import os

# retrieve environment variables
try:
    env_send_from = os.getenv('MAILFROM')
    env_send_to = os.getenv('MAILTO').split(";")
    env_password = os.getenv('MAILPASSWORD')
except:
    print('Unable to retrieve environment variables')
    return


# prepare table
try:
    body = get_email_body(
        archive_file_path = "./output/boliga.csv", 
        market_days_old = 4
    )
except:
    print('Unable to read and prepare table from archive')

# send email
send_ssl_mail(
    send_from = env_send_from, 
    password = env_password,
    subject = "Boliga Listings",
    body = body 
    server = "smtp.gmail.com"
    port = 465, 
    send_to = env_send_to
)
