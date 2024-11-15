from fastapi import APIRouter, Depends, Path, Query

from models.film import FilmworkList
from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_streaming_bulk
router = APIRouter(tags=['films'])


@router.get(
    '/films',
    #response_model=FilmworkList,
)
async def films(elastic: AsyncElasticsearch = Depends(get_elastic)):
    result = await elastic.search(index='movie', body={"query": {"match_all": {}}})
    return result
    #return {'status': 'ok'}
