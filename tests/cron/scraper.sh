#!/usr/bin/env bash
#!/bin/sh

# set env variables
export MAILTO=
export MAILFROM=
export MAILPASSWORD=

# print cwd
cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD

# print date
echo `date`

# run job
export PATH="$HOME/.poetry/bin:$PATH"
cd /home/pi/boliga-scraper
make run
echo "-----------"
