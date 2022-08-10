import asyncio

import backoff
from elasticsearch import AsyncElasticsearch, ConnectionError

from functional.settings import TestSettings

settings = TestSettings()


@backoff.on_exception(backoff.expo, ConnectionError)
async def ping(es):
    if not await es.ping():
        raise ConnectionError('ConnectionError')


async def run_test():
    es = AsyncElasticsearch(
        hosts=[f'http://{settings.es_host}:{settings.es_port}'],
        http_auth=(
            settings.es_user,
            settings.es_password
        )
    )
    await ping(es)
    await es.close()


if __name__ == '__main__':
    asyncio.run(run_test())
