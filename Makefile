ZIPCODES := 3450 2800

test:
	poetry run pytest

compose:
	poetry run python ./src/compose.py ${ZIPCODES}
