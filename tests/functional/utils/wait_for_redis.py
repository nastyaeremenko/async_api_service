import asyncio

import aioredis
import backoff
from functional.settings import TestSettings

settings = TestSettings()


@backoff.on_exception(backoff.expo, aioredis.exceptions.ConnectionError)
async def ping(redis):
    if not await redis.ping():
        raise aioredis.exceptions.ConnectionError


async def run_test():
    redis = aioredis.from_url(
        f'redis://{settings.redis_host}:{settings.redis_port}'
    )
    await ping(redis)
    await redis.close()


if __name__ == '__main__':
    asyncio.run(run_test())
