IMAGE_NAME = boliga-scraper
IMAGE_TAG = latest
PI_IP = 192.168.1.35
PI_FOLDER = scraper

local-run:
	poetry run python ./src/scraper

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run: docker-build
	docker run -it -v $(CURDIR)/output:/app/output -p $(HOST_LISTEN_PORT):5000 $(IMAGE_NAME):$(IMAGE_TAG)

docker-bash:
	docker run --rm -it -v $(CURDIR)/output:/app/output --entrypoint bash $(IMAGE_NAME):$(IMAGE_TAG)

docker-save-to-pi:
	docker save --output $(IMAGE_NAME).tar $(IMAGE_NAME)
	scp $(IMAGE_NAME).tar Makefile pi@$(PI_IP):./scraper
	rm $(IMAGE_NAME).tar

docker-load:
	docker load --input $(IMAGE_NAME).tar
