data:
	poetry run python ./scripts/run_extract_transform.py

reporting:
	poetry run python ./scripts/load_send.py

dataframe:
	poetry run python ./scripts/print_data.py

run: data reporting
