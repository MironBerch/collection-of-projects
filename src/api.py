from __future__ import unicode_literals

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI()

# Хранилище сессий в памяти
sessionStorage = {}


@app.post('/')
async def main(request: Request) -> JSONResponse:
    # Парсим входящий JSON
    request = await request.json()

    # Формируем базовую структуру ответа
    response = {
        'version': request['version'],
        'session': request['session'],
        'response': {'end_session': False},
    }

    # Обрабатываем диалог
    handle_dialog(request, response)

    return JSONResponse(content=response)


def handle_dialog(request: Request, response: dict[str, Any]) -> None:
    user_id = request['session']['user_id']

    if request['session']['new']:
        # Инициализация новой сессии
        sessionStorage[user_id] = {
            'suggests': [
                'Не хочу.',
                'Не буду.',
                'Отстань!',
            ]
        }
        response['response']['text'] = 'Привет! Купи слона!'
        return

    # Обработка согласия пользователя
    if request['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        response['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        response['response']['end_session'] = True
        return

    # Стандартный ответ
    response['response']['text'] = 'Все говорят , а ты купи слона!'


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
