from pydantic import BaseModel


class Country(BaseModel):
    name: str
    alpha2: str
    alpha3: str
    region: str
