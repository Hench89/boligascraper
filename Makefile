raw:
	poetry run python ./scripts/make_raw.py

clean:
	poetry run python ./scripts/make_clean.py

baseline:
	poetry run python ./scripts/make_baseline.py

report:
	poetry run python ./scripts/make_report.py

data: raw clean baseline

run: data report
