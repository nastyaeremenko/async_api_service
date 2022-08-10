import uuid
from datetime import date
from typing import Optional

from models.base import OrjsonBase
from models.genre import GenreBase
from models.person import PersonBase


class FilmWork(OrjsonBase):
    id: uuid.UUID
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    age_limit: Optional[int]
    imdb_rating: Optional[float]
    genres: list[GenreBase] = []
    actors: list[PersonBase] = []
    writers: list[PersonBase] = []
    directors: list[PersonBase] = []
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    directors_names: Optional[list[str]]
