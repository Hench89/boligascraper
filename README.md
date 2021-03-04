# BoligaScraper

This is a small tool to run through boliga.
The tool will apply webscraping of Boliga.dk to fetch all listings in Region Hovedstaden,
The result will be parsed into excel file

## running on Debian

to run on debian like systems, you need following packages

* language-pack-da (sudo dpkg-reconfigure locales)
* libxml2-dev + libxslt-dev (required for lxml)


## running on docker

The project includes dockerfile to run in container.

downgraded version of docker (https://github.com/portainer/portainer/issues/4585#issuecomment-751729241)
curl -sSL https://get.docker.com | sed 's/docker-ce/docker-ce=5:19.03.13~3-0~raspbian-buster/' | sh

## secrets
for debian: set environment variables in ~/.bashrc script