from django.db import connection

from api.models import Country


def setup_countries() -> None:
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM countries')
        rows = cursor.fetchall()
        for row in rows:
            country = Country(
                name=row[1],
                alpha2=row[2],
                alpha3=row[3],
                region=row[4],
            )
            country.save()
