scrape:
	poetry run python ./scripts/run_scraping.py

reporting:
	poetry run python ./scripts/send_email.py

run: scrape reporting
