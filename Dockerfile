# syntax=docker/dockerfile:1

FROM python:3.10-buster

LABEL org.opencontainers.image.source="https://github.com/northpowered/SimpleSLA"

LABEL version="2.0.2"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "main.py" , "--config=config.yml"]