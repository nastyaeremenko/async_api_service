import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films, genres, persons
from core import config
from db import elastic
from db import redis

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=f'{config.PROJECT_NAME}. Read-only API для онлайн-кинотеатра',
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    description='Информация о фильмах, жанрах и людях, участвовавших в создании произведения',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    # Подключиться можем при работающем event-loop
    # Поэтому логика подключения происходит в асинхронной функции
    redis.redis = aioredis.from_url(
        f'redis://{config.REDIS_HOST}:{config.REDIS_PORT}'
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f'http://{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'],
        http_auth=(
            config.ELASTIC_USER,
            config.ELASTIC_PASSWORD
        )
    )


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix='/api/v1/films')
app.include_router(persons.router, prefix='/api/v1/persons')
app.include_router(genres.router, prefix='/api/v1/genres')
