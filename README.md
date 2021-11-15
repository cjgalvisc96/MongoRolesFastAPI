# MongoRolesFastAPI
 This app implement a RBAC (role based access control) authentication and authorization service for your application ecosystem, using FastAPI and Mongo (using async db with Motor).
 This is a little adapation from https://github.com/tsatsujnr139/fastapi-role-based-access-control-auth-service

## Installation

##### requirements
    [Docker] https://docs.docker.com/engine/install/
    [DockerCompose] https://docs.docker.com/compose/install/

0. Create ".env" file in [DirProject] using ".env.example" file

1. Build Docker
   ```sh
    >>[DirProject] docker-compose build
   ```
2. Run Docker
   ```sh
    >>[DirProject] docker-compose up
   ```

## Usage

1. Check all routes for usage:
    ```sh
    [POST] http://127.0.0.1:8000/docs/
    ```


## Unit Tests

1. For run the test & coverage (see all test in folder tests/*):

    ```sh
    >>[DirProject] docker-compose run web pytest --cov=app/ tests --disable-warnings
    ```
   


## Tech
The technologies used for this project were the following:
* [Python3] https://www.python.org/
* [fastaapi] https://fastapi.tiangolo.com/
* [mongo] https://www.mongodb.com/
* [motor] https://motor.readthedocs.io/en/stable/
* [umongo] https://umongo.readthedocs.io/en/latest/
* [pytest] https://docs.pytest.org/en/
* [Docker] https://docs.docker.com/
