import asyncio
import json
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest as pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy

from .settings import TestSettings
from .testdata.genres_data import data as genres_data
from .testdata.index_elastic import elastic_index
from .testdata.movies_data import data as movies_data
from .testdata.persons_data import data as persons_data

settings = TestSettings()

data = {
    'movies': movies_data,
    'persons': persons_data,
    'genres': genres_data
}

API_URL = 'http://{}:{}{}'.format(settings.app_host, settings.app_port,
                                  settings.api_version)

pytestmark = pytest.mark.asyncio


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str,
                    params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = '{}{}'.format(API_URL, method)
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(
        hosts=[f'http://{settings.es_host}:{settings.es_port}'],
        http_auth=(
            settings.es_user,
            settings.es_password
        )
    )
    yield client
    await client.close()


@pytest.fixture(scope="session")
async def redis_client():
    redis = await aioredis.from_url(
        f'redis://{settings.redis_host}:{settings.redis_port}'
    )
    yield redis
    await redis.close()


async def create_index(client, index):
    if not await client.indices.exists(
            index=index
    ):
        index_data = elastic_index[index]
        await client.indices.create(
            **index_data,
            ignore=[400, 404]
        )


async def gendata(index, index_data):
    for item in index_data:
        yield {
            '_index': index,
            '_id': item['id'],
            '_source': json.dumps(item)
        }


async def load_data_to_elastic(client, index):
    fixture = data[index]
    await async_bulk(client, gendata(index, fixture))


async def init_data_to_index(client, index):
    await create_index(client, index)
    await load_data_to_elastic(client, index)
    await asyncio.sleep(1)


async def del_data_to_index(es_client, index):
    await es_client.indices.delete(index=index, ignore=[400, 404])


@pytest.fixture(scope="session")
async def initialize_environment(es_client, redis_client):
    for index in settings.elastic_index:
        await init_data_to_index(es_client, index)
    await redis_client.flushall()
    await asyncio.sleep(1)
    yield
    await redis_client.flushall()
    for index in settings.elastic_index:
        await es_client.indices.delete(index=index, ignore=[400, 404])


@pytest.fixture(scope='module')
async def create_data_person(es_client, redis_client, redis_flush):
    index = 'persons'
    await init_data_to_index(es_client, index)
    yield
    await es_client.indices.delete(index=index, ignore=[400, 404])


@pytest.fixture(scope='module')
async def create_data_movies(es_client, redis_client, redis_flush):
    index = 'movies'
    await init_data_to_index(es_client, index)
    yield
    await es_client.indices.delete(index=index, ignore=[400, 404])


@pytest.fixture(scope='module')
async def create_data_genres(es_client, redis_client, redis_flush):
    index = 'genres'
    await init_data_to_index(es_client, index)
    yield
    await del_data_to_index(es_client, index)


@pytest.fixture(scope='module')
async def redis_flush(redis_client):
    await redis_client.flushall()
    yield
    await redis_client.flushall()
