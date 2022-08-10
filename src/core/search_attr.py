from enum import Enum


class SearchAttributes(Enum):
    movies = ['title', 'description', 'actors_names',
              'writers_names', 'directors_names', 'genres_names']

    persons = ['name']
