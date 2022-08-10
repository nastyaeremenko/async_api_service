from uuid import UUID
from typing import Optional

from api.v1.models.base import OrjsonBase


class FilmsList(OrjsonBase):
    uuid: UUID
    title: str
    imdb_rating: Optional[float]


class Film(FilmsList):
    description: Optional[str]
    genres: list[dict] = []
    actors: list[dict] = []
    writers: list[dict] = []
    directors: list[dict] = []
