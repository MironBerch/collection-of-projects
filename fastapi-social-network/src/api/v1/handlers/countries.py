from fastapi import APIRouter, Response, Query

from services.countryes import get_countries, get_country_by_alpha2
from schemas.countries import Country

router = APIRouter(tags=['countries'])


@router.get(
    '/countries',
    response_model=list[Country],
)
async def countries(
    region: list[str] = Query(...),
) -> Response:
    """Возвращает страны."""
    return get_countries(region)


@router.get(
    '/countries/{alpha2}',
    response_model=Country,
)
async def country_by_alpha2(alpha2: str) -> Response:
    """Возвращает страны."""
    return get_country_by_alpha2(alpha2=alpha2)
