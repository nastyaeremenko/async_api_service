from enum import Enum


class SortFilms(str, Enum):
    imdb_rating_asc = "imdb_rating"
    imdb_rating_desc = "-imdb_rating"
