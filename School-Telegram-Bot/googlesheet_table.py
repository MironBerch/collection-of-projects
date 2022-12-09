import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


YEAR = {
    '5': 'Лист5',
    '6': 'Лист6',
    '7': 'Лист7',
    '8': 'Лист8',
    '9': 'Лист9',
    '10': 'Лист10',
    '11': 'Лист11'
}

CLASS = {
    'а': 'а',
    'б': 'б',
    'в': 'в'
}


async def get_range(class_letter: str, year_study: str) -> str:
    page = YEAR[year_study]
    class_letter = CLASS[class_letter]
    if class_letter == 'а':
        columns = 'B2:C42'
    if class_letter == 'б':
        columns = 'D2:E42'
    if class_letter == 'в':
        columns = 'F2:G42'
    range_data = page + '!' + columns
    return range_data


async def view_xlsx(values_range: str):
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '1e2NCxgEcnBlwuh6VhugKXk-swmtuXsKH3qu-g77wogA'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=values_range,#range='Лист9!B1:G42',
        majorDimension='COLUMNS'
    ).execute()
    values = values['values']
    return values