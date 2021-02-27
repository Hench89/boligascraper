import smtplib


sender_email = "hench.auto@gmail.com"
rec_email = "hench.auto@gmail.com"
password = "k4f2m2tH"
message = "Hello World!"

server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(sender_email, password)

server.sendmail(sender_email, rec_email, message)