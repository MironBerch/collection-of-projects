import os
from argparse import ArgumentParser, Namespace
from pprint import pprint

import requests
from dotenv import load_dotenv


def ask(args: Namespace) -> None:
    url = 'https://api.intelligence.io.solutions/api/v1/chat/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv('IO_NET_API_KEY')}',
    }

    json_data: dict[str, str | list[dict[str, str]]] = {
        'model': 'deepseek-ai/DeepSeek-R1',
        'messages': [
            {
                'role': 'system',
                'content': 'You are a helpful AI assistant. \
                    Your answer will returned for user in sh console. \
                        Write u answer for sh console reading.',
            },
            {
                'role': 'user',
                'content': f'{args.message}',
            },
        ],
    }
    request_response = requests.post(url, headers=headers, json=json_data).json()['choices']
    request_content = request_response[0]['message']['content']
    request_content = request_content.split('</think>\n\n')[-1]
    pprint(object=request_content)


def main() -> None:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    question_parser = subparsers.add_parser('ask')
    question_parser.add_argument('-m', '--message', required=True)

    args = parser.parse_args()

    commands = {
        'ask': ask,
    }
    commands[args.command](args)


if __name__ == '__main__':
    load_dotenv()
    main()
