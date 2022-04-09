ZIPCODES := 3450 2800

compose:
	poetry run python ./src/scrape/scraper.py ${ZIPCODES}

test:
	poetry run pytest
