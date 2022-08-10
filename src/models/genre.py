import uuid
from typing import Optional

from models.base import OrjsonBase


class GenreBase(OrjsonBase):
    id: uuid.UUID
    name: str


class Genre(GenreBase):
    description: Optional[str]
    film_ids: list[uuid.UUID] = []
