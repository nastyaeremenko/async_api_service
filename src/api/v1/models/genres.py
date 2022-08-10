import uuid as uuid
from typing import Optional, List

from api.v1.models.base import OrjsonBase


class Genre(OrjsonBase):
    uuid: uuid.UUID
    name: str
    description: Optional[str]
    film_ids: List[uuid.UUID] = []
