from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.abstract_movies import MoviesService
from utils.cache import RedisCache
from utils.elastic import AsyncElastic


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> MoviesService:
    settings = {'model': Genre, 'index': 'genres'}
    return MoviesService(RedisCache(redis, **settings),
                         AsyncElastic(elastic, **settings))
