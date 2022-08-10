import orjson


def get_redis_key(**kwargs):
    return orjson.dumps(kwargs, default=lambda o: o.json()).decode()
