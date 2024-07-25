# Проектная работа: диплом

GIT: https://github.com/KseniiaKarpova/graduate_work/tree/main

Подробное описание проекта смотрите в [документации](./docs)

## Запуск проекта:
Требуется заполнить в .env
`AUTH_GOOGLE_CLIENT_ID=`
`AUTH_GOOGLE_CLIENT_SECRET=`


## Step 1 (bild project)
```bash
cp env_example .env
```

```bash

docker-compose -f docker-compose.ai.yaml -f docker-compose.main.yaml -f docker-compose.etl.yaml  up --build
```

```bash
docker exec AuthAPI alembic upgrade head 

```
## Step 2 (migration)
Заполнение базы данных из sqlite в Postgres

```bash
curl -XGET http://0.0.0.0:8877/migrate
```


## создание тестовой записи


Чтоб записать тестовое аудио (linux):

```bash
arecord -f S16_LE exmpl.wav
```
Чтоб остановить запись: `Ctrl + C`


## Api Docs
- ASR: http://localhost:8003/api/openapi
- File API: http://localhost:8002/api/openapi
- Auth API: http://localhost:8001/api/openapi
- Cinema API:http://localhost:8005/api/openapi
- TTS API:http://localhost:8004/api/openapi