from abc import ABC, abstractmethod
from typing import TypeVar

import backoff
from elasticsearch import AsyncElasticsearch, NotFoundError, ConnectionTimeout, \
    ConnectionError

from core.config import MAX_TRIES_DB, MAX_TIME_DB
from utils.api_params_to_body import make_query

M = TypeVar('M')


class AbstractDB(ABC):

    @abstractmethod
    def get_object(self, id):
        pass

    @abstractmethod
    def get_list(self, **kwargs):
        pass


class AsyncElastic(AbstractDB):
    def __init__(self, elastic: AsyncElasticsearch, model: M, index: str):
        self.elastic = elastic
        self.model = model
        self.index = index

    @backoff.on_exception(backoff.expo,
                          (ConnectionTimeout, ConnectionError),
                          max_time=MAX_TIME_DB)
    async def get_object(self, id):
        try:
            doc = await self.elastic.get(index=self.index, id=id)
        except NotFoundError:
            return None
        return self.model(**doc['_source'])

    @backoff.on_exception(backoff.expo,
                          (ConnectionTimeout, ConnectionError),
                          max_time=MAX_TIME_DB)
    async def get_list(self, **kwargs):
        body = make_query(**kwargs, index=self.index)
        try:
            docs = await self.elastic.search(body=body, index=self.index)
        except NotFoundError:
            return None
        return [self.model(**doc['_source']) for doc in docs['hits']['hits']]
