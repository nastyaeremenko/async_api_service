from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.constants import PERSON_NOT_FOUND
from api.v1.models.films import FilmsList
from api.v1.models.persons import Person
from core.config import PAGE_SIZE, PAGE_START
from services.abstract_movies import MoviesService
from services.films import get_film_service
from services.persons import get_person_service

router = APIRouter()


@router.get('/search',
            response_model=List[Person],
            summary='Поиск по персонам',
            description='Полнотекстовый поиск персон '
                        '(актеров, режиссеров, сценаристов), '
                        'участвовавших в создании фильма  '
                        'по их имени.',
            response_description='Id, имя, должность персоны и '
                                 'список id фильмов, '
                                 'в которых персона приняла участие.',
            tags=['Полнотекстовый поиск'])
async def person_search(
        query: str = Query(..., min_length=2, max_length=50),
        page_number: int = Query(PAGE_START, alias='page[number]'),
        page_size: int = Query(PAGE_SIZE, alias='page[size]'),
        person_service: MoviesService = Depends(
            get_person_service,
        ),
) -> List[Person]:
    persons = await person_service.take_all(
        query=query,
        page_number=page_number,
        page_size=page_size,
    )
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PERSON_NOT_FOUND)
    return [
        Person(
            uuid=person.id,
            name=person.name,
            role=', '.join(person.role),
            film_ids=person.film_ids
        ) for person in persons
    ]


@router.get('/{uuid}',
            response_model=Person,
            summary='Данные по персоне',
            description='Детальное описание одной персоны '
                        '(актера, режиссера, сценариста), '
                        'участвовавшей в создании фильма .',
            response_description='Id, имя, должность персоны и '
                                 'список id фильмов, '
                                 'в которых персона приняла участие.',
            tags=['Персоны'])
async def person_details(
        uuid: UUID,
        person_service: MoviesService = Depends(
            get_person_service
        ),
) -> Person:
    person = await person_service.get_by_id(id=uuid)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PERSON_NOT_FOUND)
    role = ', '.join(person.role)
    return Person(uuid=person.id, name=person.name, role=role,
                  film_ids=person.film_ids)


@router.get('/{uuid}/film',
            response_model=List[FilmsList],
            summary='Фильмы по персоне',
            description='Список фильмов, в которых принимала '
                        'участие выбранная персона, в качестве актера, '
                        'режиссера или сценариста.',
            response_description='Id, название и рейтинг фильма.',
            tags=['Персоны'])
async def person_films(
        uuid: UUID,
        page_number: int = Query(PAGE_START, alias='page[number]'),
        page_size: int = Query(PAGE_SIZE, alias='page[size]'),

        film_service: MoviesService = Depends(
            get_film_service
        ),
) -> List[FilmsList]:
    person_in_films = await film_service.take_all(person_id=uuid,
                                                  page_number=page_number,
                                                  page_size=page_size)
    if not person_in_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                            detail=PERSON_NOT_FOUND)
    return [FilmsList(
        uuid=film.id, **film.dict()
    ) for film in person_in_films]
