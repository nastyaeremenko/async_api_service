from typing import Optional, List

import pytest
from pydantic import BaseModel, Field

from tests.functional.testdata.genres_data import data
from tests.functional.conftest import pytestmark

API_URL = "/genres/"
NOT_FOUND = {'detail': 'genre not found'}
ERROR_UUID = {'detail': [{'loc': ['path', 'uuid'],
                          'msg': 'value is not a valid uuid',
                          'type': 'type_error.uuid'}]}


class Genre(BaseModel):
    id: str = Field(alias='uuid')
    name: str
    description: Optional[str]
    film_ids: List[str] = []


async def test_all_genres(create_data_genres, make_get_request):
    response = await make_get_request(API_URL)
    assert response.status == 200
    assert len(response.body) == len(data)


@pytest.mark.parametrize(
    (
            "page_number", "page_size", "count"
    ),
    (
            (0, 1000, len(data)),
            (0, 10, 10),
            (1, 10, 10),
            (0, 3, 3),
    )
)
async def test_page_genres(
        create_data_genres,
        make_get_request,
        page_size,
        page_number,
        count
):
    response = await make_get_request(
        API_URL,
        {'page[number]': page_number, 'page[size]': page_size}
    )
    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize(
    (
            "page_size", "page_number"
    ),
    (
            (3.3, 1),
            ('sdfg', 1),
            (0, 'sdfg'),
            (1, 3.3),
    )
)
async def test_error_page_genres(
        create_data_genres,
        make_get_request,
        page_size,
        page_number,

):
    response = await make_get_request(
        API_URL,
        {'page[number]': page_number, 'page[size]': page_size}
    )
    assert response.status == 422


@pytest.mark.parametrize(
    ("genre"),
    (
            (data[18]),
            (data[1]),
            (data[10]),

    )
)
async def test_genres_id(create_data_genres, make_get_request, genre):
    url = '{}{}'.format(API_URL, genre['id'])
    response = await make_get_request(url)
    assert response.status == 200
    assert genre == Genre.parse_obj(response.body).dict()


async def test_genres_not_id(create_data_genres, make_get_request):
    url = '{}{}'.format(API_URL, 'f24fd632-b1a5-4273-a835-0119bd12f820')
    response = await make_get_request(url)
    assert response.status == 404
    assert NOT_FOUND == response.body


async def test_genres_error_uuid(create_data_genres, make_get_request):
    url = '{}{}'.format(API_URL, 'stsdf32r2fr')
    response = await make_get_request(url)
    assert response.status == 422
    assert ERROR_UUID == response.body


@pytest.mark.parametrize(
    ("genre_delete"),
    (
            (data[2]),
            (data[4]),
            (data[8]),

    )
)
async def test_genres_check_cache(create_data_genres, es_client,
                                  redis_client,
                                  make_get_request, genre_delete):
    url = '{}{}'.format(API_URL, genre_delete['id'])
    response = await make_get_request(url)
    assert response.status == 200
    assert genre_delete == Genre.parse_obj(response.body).dict()

    await es_client.delete(index='genres', id=genre_delete['id'],
                           ignore=[400, 404])

    url = '{}{}'.format(API_URL, genre_delete['id'])
    response = await make_get_request(url)
    assert response.status == 200
    assert genre_delete == Genre.parse_obj(response.body).dict()

    await redis_client.flushall()

    url = '{}{}'.format(API_URL, genre_delete['id'])
    response = await make_get_request(url)
    assert response.status == 404
