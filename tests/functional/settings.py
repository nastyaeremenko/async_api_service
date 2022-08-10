from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    is_docker: bool = Field(False, env='CONTAINER')
    es_host: str = Field('localhost', env='ELASTIC_HOST')
    es_port: str = Field('9200', env='ELASTIC_PORT')
    es_user: str = Field('elastic', env='ELASTIC_USER')
    es_password: str = Field('test', env='ELASTIC_PASSWORD')

    app_host: str = Field('localhost', env='APP_HOST')
    app_port: str = Field('8000', env='APP_PORT')

    redis_host: str = Field('localhost', env='REDIS_HOST')
    redis_port: str = Field('6379', env='REDIS_PORT')

    elastic_index: tuple = Field(('movies', 'persons', 'genres'))
    api_version: str = Field('/api/v1')
