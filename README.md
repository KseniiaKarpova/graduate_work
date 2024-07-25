# Проектная работа: диплом

GIT: https://github.com/KseniiaKarpova/graduate_work/tree/main

Подробное описание проекта смотрите в [документации](./docs)

## Запуск проекта:

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
- Auth API: http://localhost:8001/api/openapi (сервис авторизации)
- File API: http://localhost:8002/api/openapi (сервис для хранения и получения файлового хранилища)
- ASR: http://localhost:8003/api/openapi (сервис преобразования голоса в текст)
- TTS API: http://localhost:8004/api/openapi (сервис преобразования текста в аудио - отдает short_name от File API)
- Assistant API: http://localhost:8005/api/openapi (Основной сервис для взаимодействия - входная точка)
- History API: http://localhost:8006/api/openapi (сервис хранения истории - используем Монго)
- Intent API: http://localhost:8007/api/openapi (сервис логики опредления намерения по тексту)
- Text2Vec API: http://localhost:8008/api/openapi (сервис поиска и хранения тектовых данных (фильмы на русском) в векторном пространстве (база данных - Qdrant) и поиск ближайщего)
- Cinema API: http://localhost:8009/api/openapi (сервис поиска фильмов на английском (база данных - Эластик))

qdrant : http://localhost:6333/dashboard#/collections