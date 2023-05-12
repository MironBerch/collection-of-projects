# Project deployment guide on a VPS server

This is a quick guide to deploying a project on a production server.

## VPS server Configuration

#### Minimum VPS server configuration:
| Accessories | Characteristics |
| ------ | ------ |
| CPU | 1 × 2000 MHz |
| RAM | 1 GB |
| Disk | 5 Gb |

#### Recommended VPS server configuration:
| Accessories | Characteristics |
| ------ | ------ |
| CPU | 2 × 2000 MHz |
| RAM | 4 GB |
| Disk | 10 GB |

## Project Deployment

- Run this command - it will install all the dependencies needed to deploy the project
```sh
sudo apt-get install git docker docker-compose vim
```

- Run this command - it will download the project from GitHub
```sh
git clone https://github.com/MironBerch/register_of_talented_students.git
```

- Run this command - it redirects to the directory with the code
```sh
cd register_of_talented_students && cd register_of_talented_students
```

- Run this command - it will create a `.env` file using vim
```sh
vim .env
```

- Example `.env` file
```dotenv
SECRET_KEY='8fajd3)on9ecoq&&8__eryh-d5sz@6!8ky3+y0u5k6gw8!q$^t'
DEBUG=0
```

- Run this command - it will launch the site
```sh
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

- Run this command - it will view docker containers
```sh
docker ps
```

- Sample response
```sh
| CONTAINER ID | IMAGE | ...
| ------------ | ----------------------------------- | ---
| e87ee7777e59 | register_of_talented_students-nginx | ...
| 9b9701f23e02 | register_of_talented_students-web | ...
```

- Select the CONTAINER ID whose IMAGE is register_of_talented_students-web
- Run this command - it will launch bash inside the docker container
```sh
docker exec -it <CONTAINER_ID> bash
```

- Run this command - it will create an administrator inside the docker container
```sh
python manage.py createsuperuser
```