import pytest
from jsonschema import validate

from tests.functional.testdata.movies_data import data
from tests.functional.conftest import pytestmark

API_URL = '/films/'
NOT_FOUND_ERROR = {'detail': 'film not found'}
WRONG_UUID_FORMAT_ERROR = {
    'detail': [
        {
            'loc': [
                'path',
                'uuid'
            ],
            'msg': 'value is not a valid uuid',
            'type': 'type_error.uuid'
        }
    ]
}

FILMS_LIST_SCHEMA = {
    "type": "object",
    "properties": {
        "uuid": {"type": "string", "format": "uuid"},
        "title": {"type": "string"},
        "imdb_rating": {"type": ["number", "null"]},
    },
}

FILM_SCHEMA = {
    "type": "object",
    "properties": {
        "uuid": {"type": "string", "format": "uuid"},
        "title": {"type": "string"},
        "imdb_rating": {"type": ["number", "null"]},
        "description": {"type": ["string", "null"]},
        "genres": {"type": "array"},
        "actors": {"type": "array"},
        "writers": {"type": "array"},
        "directors": {"type": "array"},
    },
}


async def test_films_page_structure(
        create_data_movies,
        make_get_request
):
    """Функция проверки структуры выходных данных на странице /films"""
    response = await make_get_request(
        API_URL,
        {}
    )
    assert response.status == 200
    fields = set(response.body[0].keys()) - {'uuid', 'title', 'imdb_rating'}
    assert fields == set()
    assert validate(instance=response.body[0], schema=FILMS_LIST_SCHEMA) is None


@pytest.mark.parametrize(
    (
            'page_number', 'page_size', 'count'
    ),
    (
            (0, 1000, len(data)),
            (0, 5, 5),
            (1, 5, 5),
            (0, 3, 3),
    )
)
async def test_films_page_pagination(
        create_data_movies,
        make_get_request,
        page_size,
        page_number,
        count
):
    """Функция проверки количества возвращаемых фильмов на странице /films в
    зависимости от входных параметров: номера страницы и размера страницы"""
    response = await make_get_request(
        API_URL,
        {'page[number]': page_number, 'page[size]': page_size}
    )
    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize('sort', ('-imdb_rating',))
async def test_films_page_sort(
        create_data_movies,
        make_get_request,
        sort
):
    """Функция проверки сортировки фильмов на странице /films по рейтингу в
    при заданном параметре сортировки и при его отсутствии"""
    response = await make_get_request(
        API_URL,
        {'sort': sort, }
    )
    assert response.status == 200
    assert response.body[0]['imdb_rating'] == 8.7
    assert response.body[0]['imdb_rating'] >= response.body[1]['imdb_rating']


@pytest.mark.parametrize(
    (
        'genre_uuid', 'count'
    ),
    (
            ('3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff', 10),
            ('6d141ad2-d407-4252-bda4-95590aaf062a', 5),
    )
)
async def test_films_page_filter(
        create_data_movies,
        make_get_request,
        genre_uuid,
        count
):
    """Функция проверки фильтрации фильмов на странице /films по жанрам"""
    response = await make_get_request(
        API_URL,
        {'filter[genre]': genre_uuid, }
    )
    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize(
    (
        'page_number', 'page_size', 'error', 'status_code'
    ),
    (
            (2, 1000, NOT_FOUND_ERROR, 404),
            (5, 10, NOT_FOUND_ERROR, 404),
    )
)
async def test_films_page_errors(
        create_data_movies,
        make_get_request,
        page_number,
        page_size,
        error,
        status_code
):
    """Функция проверки ошибок на странице /films"""
    response = await make_get_request(
        API_URL,
        {'page[number]': page_number, 'page[size]': page_size}
    )
    assert response.status == status_code
    assert response.body == error


async def test_film_page_structure(
        create_data_movies,
        make_get_request
):
    """Функция проверки структуры выходных данных на странице /films/{film_id}"""
    response = await make_get_request(
        API_URL + data[0]['id'],
        {}
    )
    assert response.status == 200
    fields = set(response.body.keys()) - {'uuid', 'title', 'imdb_rating',
                                          'description', 'genres', 'actors',
                                          'writers', 'directors'}
    assert fields == set()
    assert validate(instance=response.body, schema=FILM_SCHEMA) is None


@pytest.mark.parametrize(
    (
        'film_uuid', 'film_title', 'count_writers'
    ),
    (
            ('9d284e83-21f0-4073-aac0-4abee51193d8', 'Star Trek: Insurrection', 3),
            ('8c10ae99-80df-4dcb-929f-2f8dcf15f994', 'Star Driver', 0),
    )
)
async def test_film_page_content(
        create_data_movies,
        make_get_request,
        film_uuid,
        film_title,
        count_writers
):
    """Функция проверки корректности поиска фильма по id
     на странице /films/{film_id}"""
    response = await make_get_request(
        API_URL + film_uuid,
        {}
    )
    assert response.status == 200
    assert response.body['uuid'] in film_uuid
    assert response.body['title'] in film_title
    assert len(response.body['writers']) == count_writers


@pytest.mark.parametrize(
    (
        'film_uuid', 'error', 'status_code'
    ),
    (
            ('9d284e83-21f0-4073-aac0-4abee51193d5', NOT_FOUND_ERROR, 404),
            ('82390230', WRONG_UUID_FORMAT_ERROR, 422),
            ('9d284e83-21f0-4073-aac0-4abee51193d19', WRONG_UUID_FORMAT_ERROR, 422),
    )
)
async def test_film_page_errors(
        create_data_movies,
        make_get_request,
        film_uuid,
        error,
        status_code
):
    """Функция проверки ошибок при передаче некорректного id фильма
     на странице /films/{film_id}"""
    response = await make_get_request(
        API_URL + film_uuid,
        {}
    )
    assert response.status == status_code
    assert response.body == error


async def test_films_search_page_structure(
        create_data_movies,
        make_get_request
):
    """Функция проверки структуры выходных данных на странице /films/search"""
    response = await make_get_request(
        API_URL + 'search',
        {}
    )
    assert response.status == 200
    fields = set(response.body[0].keys()) - {'uuid', 'title', 'imdb_rating'}
    assert fields == set()
    assert validate(instance=response.body[0], schema=FILMS_LIST_SCHEMA) is None


@pytest.mark.parametrize(
    (
            'page_number', 'page_size', 'count'
    ),
    (
            (0, 1000, len(data)),
            (0, 5, 5),
            (1, 5, 5),
            (0, 3, 3),
    )
)
async def test_films_search_page_pagination(
        create_data_movies,
        make_get_request,
        page_size,
        page_number,
        count
):
    """Функция проверки количества возвращаемых фильмов на странице /films/search в
    зависимости от входных параметров: номера страницы и размера страницы"""
    response = await make_get_request(
        API_URL + 'search',
        {'page[number]': page_number, 'page[size]': page_size}
    )
    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize(
    (
            'query', 'count'
    ),
    (
            ('video', 3),
            ('Documentary', 4),
            ('star', 29),
            ('stan', 29),
            ('black', 3),
    )
)
async def test_films_search_page_query(
        create_data_movies,
        make_get_request,
        query,
        count
):
    """Функция проверки поиска по строке на странице /films/search"""
    response = await make_get_request(
        API_URL + 'search',
        {'page[size]': 1000, 'query': query}
    )
    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize(
    (
            'query', 'code'
    ),
    (
            ('perfect', 404),
            ('Cruise', 404),
            ('star', 200),
    )
)
async def test_films_search_page_query_errors(
        create_data_movies,
        make_get_request,
        query,
        code
):
    """Функция проверки ошибок поиска по строке на странице /films/search"""
    response = await make_get_request(
        API_URL + 'search',
        {'page[size]': 1000, 'query': query}
    )
    assert response.status == code
