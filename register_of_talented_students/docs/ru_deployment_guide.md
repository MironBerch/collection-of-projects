# Руководство по развёртыванию проекта на VPS сервере

Это краткое руководство по развёртыванию проекта на производственный сервере.

## Конфигурация VPS сервера

#### Минимальная конфигурация VPS сервера:
| Комплектующие | Характеристика |
| ------ | ------ |
| CPU | 1 × 2000 МГц |
| RAM | 1 Гб |
| Диск | 5 Гб |

#### Рекомендуемая конфигурация VPS сервера:
| Комплектующие | Характеристика |
| ------ | ------ |
| CPU | 2 × 2000 МГц |
| RAM | 4 Гб |
| Диск | 10 Гб |

## Развёртывание проекта

- Запустите эту команду - она установит все зависимости необходимые для развёртывания проекта
```sh
sudo apt-get install git docker docker-compose vim
```

- Запустите эту команду - она скачает проект с GitHub
```sh
git clone https://github.com/MironBerch/register_of_talented_students.git
```

- Запустите эту команду - она перенаправляет в каталог с кодом
```sh
cd register_of_talented_students && cd register_of_talented_students
```

- Запустите эту команду - она создаст `.env` файл с помощью vim 
```sh
vim .env
```

- Пример `.env` файла
```dotenv
SECRET_KEY='8fajd3)on9ecoq&&8__eryh-d5sz@6!8ky3+y0u5k6gw8!q$^t'
DEBUG=0
```

- Запустите эту команду - она запустит сайт 
```sh
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

- Запустите эту команду - она просмотрит docker контейнеры
```sh
docker ps
```

- Пример ответа
```sh
| CONTAINER ID |                IMAGE                | ... 
| ------------ | ----------------------------------- | --- 
| e87ee7777e59 | register_of_talented_students-nginx | ...
| 9b9701f23e02 | register_of_talented_students-web   | ...
```

- Выберете CONTAINER ID IMAGE которого register_of_talented_students-web
- Запустите эту команду - она запустит bash внутри docker контейнера
```sh
docker exec -it <CONTAINER_ID> bash
```

- Запустите эту команду - она создаст администратора внутри docker контейнера
```sh
python manage.py createsuperuser
```