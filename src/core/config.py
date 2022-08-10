import os
from logging import config as logging_config

from dotenv import load_dotenv

from core.logger import LOGGING

load_dotenv()
# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', os.getenv('PROJECT_NAME'))

# Настройки Redis
REDIS_HOST = os.getenv('REDIS_HOST', os.getenv('REDIS_HOST'))
REDIS_PORT = int(os.getenv('REDIS_PORT', os.getenv('REDIS_PORT')))

# Настройки Elasticsearch
ELASTIC_HOST = os.getenv('ELASTIC_HOST', os.getenv('ELASTIC_HOST'))
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', os.getenv('ELASTIC_PORT')))
ELASTIC_USER = os.environ.get('ELASTIC_USER')
ELASTIC_PASSWORD = os.environ.get('ELASTIC_PASSWORD')

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CACHE_EXPIRE_IN_SECONDS = 60 * 5

PAGE_SIZE = 50
PAGE_START = 0

MAX_TRIES_DB = 3
MAX_TIME_DB = 30
