import logging
from time import sleep

from elasticsearch import AsyncElasticsearch

logger = logging.getLogger('elastic')

elastic: AsyncElasticsearch | None = None


SETTINGS = {
    'refresh_interval': '1s',
    'analysis': {
        'filter': {
            'english_stop': {
                'type': 'stop',
                'stopwords': '_english_',
            },
            'english_stemmer': {
                'type': 'stemmer',
                'language': 'english',
            },
            'english_possessive_stemmer': {
                'type': 'stemmer',
                'language': 'possessive_english',
            },
            'russian_stop': {
                'type': 'stop',
                'stopwords': '_russian_',
            },
            'russian_stemmer': {
                'type': 'stemmer',
                'language': 'russian',
            },
        },
        'analyzer': {
            'ru_en': {
                'tokenizer': 'standard',
                'filter': [
                    'lowercase',
                    'english_stop',
                    'english_stemmer',
                    'english_possessive_stemmer',
                    'russian_stop',
                    'russian_stemmer',
                ],
            },
        },
    },
}

INDICES = {
    'movies': {
        'id': {'type': 'keyword'},
        'rating': {'type': 'float'},
        'genre': {'type': 'keyword'},
        'title': {
            'type': 'text',
            'analyzer': 'ru_en',
            'fields': {'raw': {'type': 'keyword'}},
        },
        'description': {'type': 'text', 'analyzer': 'ru_en'},
        'directors_names': {'type': 'text', 'analyzer': 'ru_en'},
        'actors_names': {'type': 'text', 'analyzer': 'ru_en'},
        'writers_names': {'type': 'text', 'analyzer': 'ru_en'},
        'actors': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {'type': 'keyword'},
                'name': {'type': 'text', 'analyzer': 'ru_en'},
            },
        },
        'writers': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {'type': 'keyword'},
                'name': {'type': 'text', 'analyzer': 'ru_en'},
            },
        },
        'directors': {
            'type': 'nested',
            'dynamic': 'strict',
            'properties': {
                'id': {'type': 'keyword'},
                'name': {'type': 'text', 'analyzer': 'ru_en'},
            },
        },
    },
    'persons': {
        'id': {'type': 'keyword'},
        'full_name': {
            'type': 'text',
            'analyzer': 'ru_en',
            'fields': {'raw': {'type': 'keyword'}},
        },
    },
    'genres': {
        'id': {'type': 'keyword'},
        'name': {
            'type': 'text',
            'analyzer': 'ru_en',
            'fields': {'raw': {'type': 'keyword'}},
        },
        'description': {'type': 'text', 'analyzer': 'ru_en'},
    },
}


async def get_elastic() -> AsyncElasticsearch | None:
    return elastic


async def create_indexes() -> None:
    """Создаёт индексы с соответствующими настройками и схемой данных."""
    sleep(30)
    for index, properties in INDICES.items():
        if not await elastic.indices.exists(index=index):
            body = {
                'settings': SETTINGS,
                'mappings': {
                    'dynamic': 'strict',
                    'properties': properties,
                },
            }
            await elastic.indices.create(index=index, body=body)
    logger.info('Indexes created successfully')
