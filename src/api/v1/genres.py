from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.constants import GENRE_NOT_FOUND
from api.v1.models.genres import Genre
from core.config import PAGE_START, PAGE_SIZE
from services.abstract_movies import MoviesService
from services.genre import get_genre_service

router = APIRouter()


@router.get('/',
            response_model=List[Genre],
            summary='Список жанров',
            description='Список жанров фильмов с пагинацией '
                        'по номеру и размеру страницы.',
            response_description='Id, название, описание жанра и '
                                 'список id фильмов этого жанра.',
            tags=['Жанры'])
async def get_genres(
        page_number: int = Query(PAGE_START, alias='page[number]'),
        page_size: int = Query(PAGE_SIZE, alias='page[size]'),
        genre_service: MoviesService = Depends(
            get_genre_service
        )
) -> List[Genre]:
    genres = await genre_service.take_all(page_number=page_number,
                                          page_size=page_size)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=GENRE_NOT_FOUND)
    return [Genre(uuid=genre.id, **genre.dict()) for genre in genres]


@router.get('/{uuid}',
            response_model=Genre,
            summary='Данные по жанру',
            description='Детальное описание одного жанра.',
            response_description='Id, название, описание жанра и '
                                 'список id фильмов этого жанра.',
            tags=['Жанры'])
async def genre_details(
        uuid: UUID,
        genre_service: MoviesService = Depends(
            get_genre_service
        ),
) -> Genre:
    genre = await genre_service.get_by_id(id=uuid)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=GENRE_NOT_FOUND)
    return Genre(uuid=genre.id, **genre.dict())
