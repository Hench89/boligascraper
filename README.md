# Housing Agent

Looking into buyig a house in denmark?
This project includes a code to fetch recents listings on Boliga.dk for sale or sold.
The results are processed and cleaned into a report that can be sent to your email.


# Installation

1. Install python
2. Setup poetry for python: `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`
3. Clone repository and run `poetry install` from root folder

# How to run

Using make to document commands:
* `make data` will generate reports
* `make mails` will send generated report to email(s) configured
* `make run` will do both of the above


# Configuration

## Geo scope

Fetching data is done based on values specified in zipcodes.csv

## Emails

To send data to an email address, use the send_ssl_mail function from reporting.emails module.
`send_ssl_mail(send_from, password, subject, body, server, port, send_to)`
See file scripts/send_email.py for an example.

Important: set secrets in environment variables

* MAILFROM: sender email
* MAILPASSWORD: sender password
* MAILTO: recipients list, semi-colon (;) separated

## Setting up a cronjob

The code can be run through linux cronjob (e.g. on a raspberry pi) using crontab.
See attached script/cron/ for an example that:

* runs the job every day at 15:00
* calls a bash script to run the code correctly
* logs outputs into out.txt for debugging
