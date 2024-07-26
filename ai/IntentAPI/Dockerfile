FROM python:3.10

ENV TZ=Europe/Moscow

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
     && pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y gettext && apt-get install -y netcat-traditional

COPY ./entrypoint.sh /
RUN chmod 777 /entrypoint.sh

COPY . /app
ENTRYPOINT ["/entrypoint.sh"]