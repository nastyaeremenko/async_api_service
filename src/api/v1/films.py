from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.constants import FILM_NOT_FOUND
from api.v1.filters.films_filter import Filters, get_films_filters
from api.v1.models.films import Film, FilmsList
from api.v1.sort.films_sort import SortFilms
from core.config import PAGE_START, PAGE_SIZE
from services.abstract_movies import MoviesService
from services.films import get_film_service

router = APIRouter()


@router.get('/',
            response_model=list[FilmsList],
            summary='Список фильмов',
            description='Список фильмов с возможностью '
                        'сортировки по рейтингу, фильтрации по id жанра и '
                        'пагинацией (можно задать размер страницы и номер страницы).',
            response_description='Id, название и рейтинг фильма.',
            tags=['Фильмы']
            )
async def films_list(page_number: int = Query(PAGE_START, alias='page[number]'),
                     page_size: int = Query(PAGE_SIZE, alias='page[size]'),
                     sort: Optional[SortFilms] = Query(None),
                     filters: Filters = Depends(get_films_filters),
                     film_service: MoviesService = Depends(get_film_service)) -> list[FilmsList]:

    films = await film_service.take_all(page_number=page_number, page_size=page_size,
                                        sort=sort, filters=filters)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return [FilmsList(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating,
                      description=film.description, actors=film.actors,
                      writers=film.writers,
                      genres=film.genres, directors=film.directors)
            for film in films]


@router.get('/search', 
            response_model=list[FilmsList],
            summary='Поиск по фильмам',
            description='Полнотекстовый поиск фильма по названию, '
                        'жанру и людям, участвующих в его создании.',
            response_description='Id, название и рейтинг фильма.',
            tags=['Полнотекстовый поиск']
            )
async def films_search(query: Optional[str] = Query(None, min_length=2, max_length=100),
                       page_number: int = Query(PAGE_START, alias='page[number]'),
                       page_size: int = Query(PAGE_SIZE, alias='page[size]'),
                       sort: Optional[SortFilms] = Query(None),
                       filters: Filters = Depends(get_films_filters),
                       film_service: MoviesService = Depends(get_film_service)) -> list[FilmsList]:
    films = await film_service.take_all(page_number=page_number, page_size=page_size,
                                        sort=sort, filters=filters, query=query)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return [FilmsList(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating,
                      description=film.description, actors=film.actors,
                      writers=film.writers,
                      genres=film.genres, directors=film.directors)
            for film in films]


@router.get('/{uuid}', 
            response_model=Film,
            summary='Данные по фильму',
            description='Детальное описание фильма.',
            response_description='Id, название, рейтинг, описание, жары, '
                                 'актеры, сценаристы, режиссеры фильма.',
            tags=['Фильмы'])
async def film_details(uuid: UUID = Query(None, alias='<uuid:UUID>'),
                       film_service: MoviesService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(id=uuid)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=FILM_NOT_FOUND)
    return Film(uuid=film.id, title=film.title, imdb_rating=film.imdb_rating,
                description=film.description, actors=film.actors,
                writers=film.writers,
                genres=film.genres, directors=film.directors)
