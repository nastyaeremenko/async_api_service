import uuid
from typing import Union, List, Optional

from models.base import OrjsonBase


class PersonBase(OrjsonBase):
    id: uuid.UUID
    name: str


class Person(PersonBase):
    role: Union[str, List] = ''
    film_ids: Optional[List] = []
