import uuid
from abc import ABC, abstractmethod

from utils.cache import AbstractCache, movies_cache
from utils.elastic import AbstractDB


class AbstractService(ABC):

    @abstractmethod
    def get_from_cache(self, id):
        pass

    @abstractmethod
    def set_to_cache(self, **kwargs):
        pass


class MoviesService:
    def __init__(self, cache: AbstractCache, db: AbstractDB):
        self.cache = cache
        self.db = db

    @movies_cache
    async def get_by_id(self, id: uuid.UUID):
        obj = await self.db.get_object(id)
        if not obj:
            return None
        return obj

    @movies_cache
    async def take_all(self, **kwargs):
        objects = await self.db.get_list(**kwargs)
        if not objects:
            return None
        return objects
