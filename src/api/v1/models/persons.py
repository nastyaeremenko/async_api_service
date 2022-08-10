import uuid
from typing import Optional, List

from api.v1.models.base import OrjsonBase


class Person(OrjsonBase):
    uuid: uuid.UUID
    name: str
    role: Optional[str] = ''
    film_ids: Optional[List] = []
