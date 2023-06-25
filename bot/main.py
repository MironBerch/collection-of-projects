import time
import json

import requests

from consts import TOKEN, URL, SLEEP_TIME


def get_updates(offset: int = 0) -> list:
    result: dict = (
        requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    )
    return result['result']


def send_message(chat_id: int, text: str) -> None:
    requests.get(
        f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={text}',
    )


def send_photo_url(chat_id: int, img_url: str) -> None:
    requests.get(
        f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}'
    )


def send_photo_file(chat_id: int, img: str) -> None:
    files = {'photo': open(img, 'rb')}
    requests.post(
        f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}',
        files=files,
    )


def inline_keyboard(chat_id: int, text: str) -> None:
    reply_markup: dict = {
        'inline_keyboard': [
            [
                {
                    'text': 'my github profile',
                    'url': 'https://github.com/MironBerch/',
                },
            ],
        ],
    }
    data: dict = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': json.dumps(reply_markup),
    }
    requests.post(
        f'{URL}{TOKEN}/sendMessage',
        data=data,
    )


def reply_keyboard(chat_id: int, text: str) -> None:
    reply_markup: dict = {
        'keyboard': [
            ['photo by url', 'photo from pc', 'github'],
            ['hello']
        ],
        'resize_keyboard': True,
        'one_time_keyboard': True,
    }
    data = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': json.dumps(reply_markup),
    }
    requests.post(
        f'{URL}{TOKEN}/sendMessage',
        data=data
    )


def check_message(chat_id: int, message: str) -> None:
    if message.lower() in ['hello', 'hi', '/start']:
        send_message(chat_id, 'Hello')
    elif message.lower() in 'github':
        inline_keyboard(chat_id, 'my github profile')
    elif message.lower() in 'photo by url':
        send_photo_url(
            chat_id,
            'https://avatars.githubusercontent.com/u/106734953',
        )
    elif message.lower() in 'photo from pc':
        send_photo_file(chat_id, 'photo.jpg')
    else:
        reply_keyboard(
            chat_id,
            'commands: /start | hello | hi | github | photo by url | photo from pc'
        )


def run() -> None:
    update_id = get_updates()[-1]['update_id']
    while True:
        time.sleep(SLEEP_TIME)
        messages = get_updates(update_id)
        for message in messages:
            if update_id < message['update_id']:
                update_id = message['update_id']
                if (user_message := message['message'].get('text')):
                    check_message(
                        message['message']['chat']['id'],
                        user_message,
                    )


if __name__ == '__main__':
    run()
