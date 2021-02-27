IMAGE_NAME = boliga-scraper
IMAGE_TAG = latest

local-run:
	poetry run python ./src/scraper

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run: docker-build
	docker run -it -v $(CURDIR)/output:/app/output -p $(HOST_LISTEN_PORT):5000 $(IMAGE_NAME):$(IMAGE_TAG)

docker-bash:
	docker run --rm -it -v $(CURDIR)/output:/app/output --entrypoint bash $(IMAGE_NAME):$(IMAGE_TAG)
