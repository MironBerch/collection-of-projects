from schemas.countries import Country

from db.database import create_connection, create_cursor


def get_country_by_alpha2(alpha2: str) -> Country:
    connection = create_connection()
    cursor = create_cursor(connection)
    cursor.execute(f'SELECT * FROM countries WHERE alpha2=\'{alpha2}\';')
    country = cursor.fetchone()
    cursor.close()
    connection.close()
    return Country(name=country[1], alpha2=country[2], alpha3=country[3], region=country[4])


def get_countries(regions) -> list[Country]:
    connection = create_connection()
    cursor = create_cursor(connection)
    cursor.execute('SELECT * FROM countries WHERE region IN %s;', (tuple(regions),))
    countries = [
        Country(
            name=country[1],
            alpha2=country[2],
            alpha3=country[3],
            region=country[4],
        ) for country in cursor.fetchall()
    ]
    cursor.close()
    connection.close()
    return countries
