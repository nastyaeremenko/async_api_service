from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film_work import FilmWork
from services.abstract_movies import MoviesService
from utils.cache import RedisCache
from utils.elastic import AsyncElastic


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> MoviesService:
    settings = {'model': FilmWork, 'index': 'movies'}
    return MoviesService(RedisCache(redis, **settings),
                         AsyncElastic(elastic, **settings))
