IMAGE_NAME = boliga-scraper
IMAGE_TAG = latest
PI_IP = 192.168.1.35
PI_FOLDER = scraper

scrape:
	poetry run python ./src/scraper

reporting:
	poetry run python ./src/reporting

run: scrape reporting

docker-build:
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	rm requirements

docker-run: docker-build
	docker run -it -v $(CURDIR)/output:/app/output -p $(HOST_LISTEN_PORT):5000 $(IMAGE_NAME):$(IMAGE_TAG)

docker-bash:
	docker run --rm -it -v $(CURDIR)/output:/app/output --entrypoint bash $(IMAGE_NAME):$(IMAGE_TAG)

docker-send-bin-to-pi:
	scp $(IMAGE_NAME).tar Makefile pi@$(PI_IP):./scraper
	rm $(IMAGE_NAME).tar
