ZIPCODES := 3450 2800

compose:
	poetry run python ./src/compose.py ${ZIPCODES}

test:
	poetry run pytest
