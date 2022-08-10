import functools
import json
from abc import ABC, abstractmethod
from typing import TypeVar

import backoff
from aioredis import Redis, ConnectionError, TimeoutError

from core.config import CACHE_EXPIRE_IN_SECONDS, MAX_TRIES_DB, MAX_TIME_DB
from utils.get_redis_key import get_redis_key


class AbstractCache(ABC):

    @abstractmethod
    def get_from_cache(self, key):
        pass

    @abstractmethod
    def set_to_cache(self, key, value):
        pass


M = TypeVar('M')


class RedisCache(AbstractCache):
    def __init__(self, cache: Redis, model: M, index: str):
        self.cache = cache
        self.model = model
        self.index = index

    @backoff.on_exception(backoff.expo,
                          (ConnectionError, TimeoutError),
                          max_time=MAX_TIME_DB)
    async def get_from_cache(self, key):
        data = await self.cache.get(str(key))
        if not data:
            return None
        data = json.loads(data.decode())
        if isinstance(data, list):
            return [self.model.parse_raw(item) for item in data]
        return self.model.parse_raw(data)

    @backoff.on_exception(backoff.expo,
                          (ConnectionError, TimeoutError),
                          max_time=MAX_TIME_DB)
    async def set_to_cache(self, key, value):
        value = json.dumps(value, default=lambda obj: obj.json())
        await self.cache.set(str(key), value, CACHE_EXPIRE_IN_SECONDS)


def movies_cache(func):
    @functools.wraps(func)
    async def wrapper(obj, **kwargs):
        key = get_redis_key(es_model=obj.cache.index, **kwargs)
        data = await obj.cache.get_from_cache(key)
        if not data:
            data = await func(obj, **kwargs)
            if not data:
                return None
            await obj.cache.set_to_cache(key, data)
        return data

    return wrapper
