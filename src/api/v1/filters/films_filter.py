import uuid
from typing import Optional

from fastapi import Query
from pydantic import BaseModel

from api.v1.models.base import OrjsonBase


class FilterParams(OrjsonBase):
    name: str
    value: Optional[uuid.UUID]
    is_dict: bool


class Filters(BaseModel):
    filter_genre: Optional[FilterParams]


def get_films_filters(
        filter_genre: Optional[uuid.UUID] = Query(None, alias="filter[genre]")
) -> Filters:
    return Filters(filter_genre=FilterParams(name='genres', value=filter_genre,
                                             is_dict=True),)
