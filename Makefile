all: scrape clean report

scrape:
	poetry run python ./src/agent/scrape.py

clean:
	poetry run python ./src/agent/clean.py

report:
	poetry run python ./src/agent/report.py
