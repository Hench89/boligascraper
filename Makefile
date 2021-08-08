all: scrape clean

scrape:
	poetry run python ./src/agent/scrape.py

clean:
	poetry run python ./src/agent/clean.py
