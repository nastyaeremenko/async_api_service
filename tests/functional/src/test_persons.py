import pytest

from tests.functional.testdata.persons_data import data
from tests.functional.conftest import pytestmark

API_URL = "/persons/"
NOT_FOUND = {'detail': 'person not found'}


async def test_search_persons(create_data_person, make_get_request):
    url = '{}{}'.format(API_URL, 'search')
    response = await make_get_request(url, params={'query': 'Robert'})
    assert response.status == 200
    assert len(response.body) == 3


@pytest.mark.parametrize(
    (
            "query", "page_number", "page_size", "count"
    ),
    (
            ('Robert', 0, 1000, 3),
            ('Robert', 0, 2, 2),
            ('Robert', 1, 2, 1),
            ('Robert', 1, 2, 1),
            ('Chris', 0, 2, 2),
            ('Chris', 0, 1000, 2),
    )
)
async def test_search_persons_page(create_data_person, make_get_request, query,
                                   page_number, page_size, count):
    url = '{}{}'.format(API_URL, 'search')
    response = await make_get_request(url, params={'query': query,
                                                   'page[number]': page_number,
                                                   'page[size]': page_size})
    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize(
    (
            "query", 'code_response'
    ),
    (
            ('Alex', 404),
            ('Ten', 404),
            ('asfsdvsd', 404),
            ('121e1', 404),
    )
)
async def test_search_not_persons(create_data_person, make_get_request, query,
                                  code_response):
    url = '{}{}'.format(API_URL, 'search')
    response = await make_get_request(url, params={'query': query})
    assert response.status == code_response


@pytest.mark.parametrize(
    ("person"),
    (
            (data[2]),
            (data[4]),
            (data[8]),

    )
)
async def test_search_persons_id(create_data_person, make_get_request, person):
    url = '{}{}'.format(API_URL, person['id'])
    response = await make_get_request(url)
    assert response.status == 200
    assert person['id'] == response.body['uuid']
    assert person['name'] == response.body['name']


@pytest.mark.parametrize(
    ("person", 'film_ids'),
    (
            (
                    '5cdb81f0-035d-4891-be02-196db0489537',
                    [
                        '3aba7aa0-8930-417c-bf78-3df596c3f062',
                        'e44b50ef-485f-46ca-973c-4c78c94b6f73'
                    ]
            ),
            (
                    'b8ef2cff-b618-4e0a-b215-76bbf417a7e2',
                    [
                        'd718c261-e954-4615-97f8-9ba67cd823a9',
                        '19d6b54f-8519-4147-baeb-125d05661395',
                        '7a25c172-c846-48b6-8cb4-e9003b786937',
                        '78566220-add4-4171-bd86-3d41a1e9cd2d'
                    ]
            ),

    )
)
async def test_persons_to_films(create_data_person, create_data_movies,
                                make_get_request, person, film_ids):
    url = '{}{}{}'.format(API_URL, person, '/film')
    response = await make_get_request(url)
    assert response.status == 200
    result = response.body
    assert len(film_ids) == len(result)
    result_fim_ids = [item['uuid'] for item in result]
    assert set(film_ids) == set(result_fim_ids)


@pytest.mark.parametrize(
    ("person"),
    (
            (data[2]),
            (data[4]),
            (data[8]),

    )
)
async def test_persons_check_cache(create_data_genres, es_client,
                                  redis_client,
                                  make_get_request, person):
    url = '{}{}'.format(API_URL, person['id'])
    response = await make_get_request(url)
    assert response.status == 200
    result = response.body
    assert person['id'] == result['uuid']
    assert person['name'] == result['name']

    await es_client.delete(index='persons', id=person['id'],
                           ignore=[400, 404])

    response = await make_get_request(url)
    assert response.status == 200
    result = response.body
    assert person['id'] == result['uuid']
    assert person['name'] == result['name']

    await redis_client.flushall()

    url = '{}{}'.format(API_URL, person['id'])
    response = await make_get_request(url)
    assert response.status == 404
