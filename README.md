# Project work of sprint 9
 

![workflowr status](https://github.com/AnnaKPolyakova/ugc_sprint_2/actions/workflows/python-publish.yml/badge.svg)

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


API for adding likes, reviews, bookmarks
Testing mongodb

Technologies and requirements:
```
Python 3.9+
mongodb
```
### Docker Settings

##### Installation

* [Detailed installation guide](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

### Docker-compose settings

##### Installation

* [Detailed Installation Guide](https://docs.docker.com/compose/install/)

### Launch the application

#### Before starting the project, create environment variables
Create a .env in the root and add the necessary variables to it
Example in .env.example - to run the entire application in docker
Example in .env.example-local - to run the application locally and partially in docker

#### Run completely in docker containers:

* `docker-compose up -d --build`
* `docker-compose -f docker-compose-logging.yml up -d --build`
* `docker-compose -f docker-compose-mongo.yml up -d --build`
* `chmod +x mongo/entrypoint.sh` - make the file executable
* `mongo/entrypoint.sh - start` creating tables on shards

To stop the container:
* `docker-compose down --rmi all --volumes`
* `docker-compose -f docker-compose-logging.yml down --rmi all --volumes`
* `docker-compose -f docker-compose-mongo.yml down --rmi all --volumes`


#### Running the project partially in docker containers

* `docker-compose -f docker-compose-logging.yml up -d --build`
* `docker-compose -f docker-compose-mongo.yml up -d --build`
* `python -m users_actions_app.app`
* `chmod +x mongo/entrypoint.sh` - make the file executable
* `mongo/entrypoint.sh - start` creating tables on shards

To stop the container:
* `docker-compose -f docker-compose-logging.yml down --rmi all --volumes`


Documentation at:
http://127.0.0.1:8080/v1/doc/redoc/ or
http://127.0.0.1:8080/v1/doc/swagger/


### Tests

Create .env_test in the root and add the necessary variables to it
Example in .env_test.example - to run the entire application in docker
Example in .env_test.example-local - to run the application locally and partially in docker

#### Run tests partially in docker containers

* `docker-compose -f tests/functional/docker-compose-test-local.yml up -d --build`

To stop the container:
* `docker-compose -f tests/functional/docker-compose-test-local.yml down --rmi all --volumes`

#### Running tests in docker containers

* `docker-compose -f tests/functional/docker-compose-test.yml up -d --build`

To stop the container:
* `docker-compose -f tests/functional/docker-compose-test.yml down --rmi all --volumes`
