data:
	poetry run python ./scripts/run_extract_transform.py

reporting:
	poetry run python ./scripts/load_send.py

run: data reporting
