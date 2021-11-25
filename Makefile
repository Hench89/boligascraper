ZIPCODES := 3450

test:
	poetry run pytest

compose:
	poetry run python ./src/compose.py ${ZIPCODES}
