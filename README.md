 # Проектная работа 9 спринта
 

![workflowr status](https://github.com/AnnaKPolyakova/ugc_sprint_2/actions/workflows/python-publish.yml/badge.svg)  

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)  


Командная работа https://github.com/AnnaKPolyakova/ugc_sprint_2

API для добавления лайков, отзывов, закладок
Тестирование mongodb

Технологии и требования:
```
Python 3.9+
mongodb
```
### Настройки Docker

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Настройки Docker-compose

##### Установка

* [Подробное руководство по установке](https://docs.docker.com/compose/install/)

### Запуск приложения

#### Перед запуском проекта создаем переменные окружения
Создаем в корне .env и добавляем в него необходимые переменные  
Пример в .env.example - для запуска приложения целиком в docker  
Пример в .env.example-local - для запуска приложения локально и частично в docker

#### Запуск полностью в контейнерах docker: 

* `docker-compose up -d --build`
* `docker-compose -f docker-compose-logging.yml up -d --build`
* `docker-compose -f docker-compose-mongo.yml up -d --build`
* `chmod +x mongo/entrypoint.sh` - делаем файл исполняемым
* `mongo/entrypoint.sh - запускаем` создание таблиц на шардах

Для остановки контейнера:  
* `docker-compose down --rmi all --volumes`
* `docker-compose -f docker-compose-logging.yml down --rmi all --volumes`
* `docker-compose -f docker-compose-mongo.yml down --rmi all --volumes`


#### Запуск проекта частично в контейнерах docker

* `docker-compose -f docker-compose-logging.yml up -d --build`
* `docker-compose -f docker-compose-mongo.yml up -d --build`
* `python -m users_actions_app.app`
* `chmod +x mongo/entrypoint.sh` - делаем файл исполняемым
* `mongo/entrypoint.sh - запускаем` создание таблиц на шардах

Для остановки контейнера:  
* `docker-compose -f docker-compose-logging.yml down --rmi all --volumes`


Документация по адресу:
http://127.0.0.1:8080/v1/doc/redoc/ или  
http://127.0.0.1:8080/v1/doc/swagger/


### Тесты

Создаем в корне .env_test и добавляем в него необходимые переменные  
Пример в .env_test.example - для запуска приложения целиком в docker  
Пример в .env_test.example-local - для запуска приложения локально и частично в docker

#### Запуск тестов частично в контейнерах docker

* `docker-compose -f tests/functional/docker-compose-test-local.yml up -d --build`

Для остановки контейнера:  
* `docker-compose -f tests/functional/docker-compose-test-local.yml down --rmi all --volumes`

#### Запуск тестов в контейнерах docker

* `docker-compose -f tests/functional/docker-compose-test.yml up -d --build`

Для остановки контейнера:  
* `docker-compose -f tests/functional/docker-compose-test.yml down --rmi all --volumes`