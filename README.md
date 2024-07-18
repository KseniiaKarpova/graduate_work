# Проектная работа: диплом

Подробное описание проекта смотрите в [документации](./docs)

## Запуск проекта:
Требуется заполнить в .env
`AUTH_GOOGLE_CLIENT_ID=`
`AUTH_GOOGLE_CLIENT_SECRET=`


```bash
cp env_example .env
```

```bash

docker-compose -f docker-compose.ai.yaml  up --build
```

```bash
docker exec AuthAPI alembic upgrade head 
```



## Test

Чтоб записать тестовое аудио (linux):

```bash
arecord -f S16_LE exmpl.wav
```
Чтоб остановить запись `Ctrl + C`


## Api Docs
- ASR: http://localhost:8003/api/openapi
- File API: http://localhost:8002/api/openapi
- Auth API: http://localhost:8001/api/openapi