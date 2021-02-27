FROM python:3.8-slim

# install poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.create false

# install dependencies
RUN mkdir -p /app/src
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-root

# copy sourcce code and install
COPY src /app/src
RUN poetry install
COPY static /app/static

# set the locale
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# da_DK.UTF-8 UTF-8/da_DK.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=da_DK.UTF-8
ENV LANG da_DK.UTF-8 

# map output folder to outside of container
RUN mkdir -p /app/output
VOLUME output /app/output


# run
CMD ["python", "./src/scraper"]
