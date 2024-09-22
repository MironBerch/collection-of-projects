from elasticsearch import AsyncElasticsearch

elastic: AsyncElasticsearch | None = None


async def get_elastic() -> AsyncElasticsearch:
    return elastic
