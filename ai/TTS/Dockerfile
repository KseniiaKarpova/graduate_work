FROM python:3.10-slim

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

COPY . /app