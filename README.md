# Boliga Scraper

This is a small tool to fetch listings from Boliga.dk
The result will be parsed into excel file

## How to Install

Prerequisites

* language-pack-da (sudo dpkg-reconfigure locales)
* Poetry for python

To install run the code `poetry install --no-dev`

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
