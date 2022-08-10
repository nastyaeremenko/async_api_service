from uuid import UUID
from core.search_attr import SearchAttributes


def make_query(page_number: int = None,
               page_size: int = None,
               sort=None,
               filters=None,
               query: str = None,
               index: str = None,
               person_id: UUID = None) -> dict:
    body = {}
    if page_size:
        body['size'] = page_size
        if page_number is not None:
            body['from'] = page_size * page_number
    if sort:
        keyword = 'asc'
        if sort.value.startswith('-'):
            keyword = 'desc'
            sort = sort.value.removeprefix('-')
        body['sort'] = {sort: keyword}
    if filters:
        for filter_key, filter_dict in filters:
            if filter_dict and filter_dict.value:
                if 'query' not in body:
                    body['query'] = {'bool': {'filter': []}}
                if filter_dict.is_dict:
                    body['query']['bool']['filter'].append({
                        'nested': {
                            'path': filter_dict.name,
                            'query': {
                                'bool': {
                                    'must': [
                                        {
                                            'term': {
                                                '{}.id'.format(filter_dict.name): filter_dict.value
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    })
    if query:
        query_dict = {'must': [{
            'multi_match': {
                'query': query,
                'fuzziness': 'auto',
                'fields': SearchAttributes[index].value
            }
        }]}
        if 'query' not in body:
            body['query'] = {'bool': query_dict}
        else:
            body['query']['bool'].update(query_dict)
    if person_id:
        person_fields = ['writers', 'directors', 'actors']
        if 'query' not in body:
            body['query'] = {'bool': {'should': []}}
        else:
            body['query']['bool'].update({'should': []})
        for field in person_fields:
            body['query']['bool']['should'].append({
                'nested': {
                    'path': field,
                    'query': {
                        'bool': {
                            'must': [
                                {
                                    'term': {
                                        '{}.id'.format(field): person_id
                                    }
                                }
                            ]
                        }
                    }
                }
            })
        if 'filter' in body['query']['bool']:
            body['query']['bool'].update({'minimum_should_match': 1})
    return body
