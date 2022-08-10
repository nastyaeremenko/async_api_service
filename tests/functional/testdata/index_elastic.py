index_settings = {
    "index": {
        "refresh_interval": "1s",
        "number_of_shards": "1",
        "analysis": {
            "filter": {
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                },
                "english_stemmer": {
                    "type": "stemmer",
                    "language": "english"
                },
                "english_possessive_stemmer": {
                    "type": "stemmer",
                    "language": "possessive_english"
                },
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "english_stop": {
                    "type": "stop",
                    "stopwords": "_english_"
                }
            },
            "analyzer": {
                "ru_en": {
                    "filter": [
                        "lowercase",
                        "english_stop",
                        "english_stemmer",
                        "english_possessive_stemmer",
                        "russian_stop",
                        "russian_stemmer"
                    ],
                    "tokenizer": "standard"
                }
            }
        },
        "number_of_replicas": "1",
    }
}

index_movies = {
    "index": "movies",
    "body": {
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "actors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "text",
                            "analyzer": "ru_en"
                        }
                    }
                },
                "actors_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "directors": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "text",
                            "analyzer": "ru_en"
                        }
                    }
                },
                "directors_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "description": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "genres": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "text",
                            "analyzer": "ru_en"
                        }
                    }
                },
                "genres_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "id": {
                    "type": "keyword"
                },
                "imdb_rating": {
                    "type": "float"
                },
                "title": {
                    "type": "text",
                    "fields": {
                        "raw": {
                            "type": "keyword"
                        }
                    },
                    "analyzer": "ru_en"
                },
                "writers": {
                    "type": "nested",
                    "dynamic": "strict",
                    "properties": {
                        "id": {
                            "type": "keyword"
                        },
                        "name": {
                            "type": "text",
                            "analyzer": "ru_en"
                        }
                    }
                },
                "writers_names": {
                    "type": "text",
                    "analyzer": "ru_en"
                }
            }
        },
        "settings": index_settings
    }
}

index_persons = {
    "index": "persons",
    "body": {
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "role": {
                    "type": "keyword"
                },
                "film_ids": {
                    "type": "keyword"
                },
            }
        },
        "settings": index_settings
    }
}
index_genres = {
    "index": "genres",
    "body": {
        "mappings": {
            "dynamic": "strict",
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "name": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "description": {
                    "type": "text",
                    "analyzer": "ru_en"
                },
                "film_ids": {
                    "type": "keyword"
                },
            }
        },
        "settings": index_settings
    }
}

elastic_index = {
    'movies': index_movies,
    'persons': index_persons,
    'genres': index_genres
}
# for name, index_setting in elastic_index.items():
#     if not self.client.indices.exists(
#             index=name
#     ):
#         self.client.indices.create(
#             **index_setting,
#             ignore=400
#         )
