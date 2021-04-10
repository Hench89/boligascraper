raw:
	poetry run python ./scripts/make_raw.py

clean:
	poetry run python ./scripts/make_clean.py

load:
	poetry run python ./scripts/make_load.py

print:
	poetry run python ./scripts/make_print.py

run: data reporting
