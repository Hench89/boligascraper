raw:
	poetry run python ./scripts/make_raw.py

clean:
	poetry run python ./scripts/make_clean.py

report:
	poetry run python ./scripts/make_report.py

mails:
	poetry run python ./scripts/make_mails.py

data: raw clean report

run: data mails
