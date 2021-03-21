# Boliga Scraper

This is a small tool to fetch listings from Boliga.dk
The result will be parsed into excel file

## How to Install

Prerequisites

* python<br>
    `sudo apt-get install python3 python3-distutils`
* language pack cnfigure to da_DK.UTF-8<br>
    `sudo dpkg-reconfigure locales`
* Poetry for python<br>
`curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`

To install run the code `make install`

## How to run scraping

To retrieve listings, use the compute function from scraper.reader module.
`df = compute(archive_path, zipcodes_path, stations_path)`
See file scripts/run_scraping.py for an example.

## How to send email

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
