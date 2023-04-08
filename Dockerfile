# $ docker build --tag gu_scraping:latest --no-cache .
# $ docker run --name GU_Scraping --volume 'ホストOS':/usr/local --workdir /usr/local --interactive --tty --detach --rm gu_scraping:latest

FROM python:3.11.3

COPY . /usr/local
VOLUME 'ホストOS' /usr/local

WORKDIR /usr/local/src

RUN apt-get update \
    && apt-get install -y libgl1-mesa-dev

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
