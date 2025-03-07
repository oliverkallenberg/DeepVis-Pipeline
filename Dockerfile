FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /data
RUN touch /data/metadata.json

COPY configs/ .
COPY scripts/ .
COPY config.yml /
