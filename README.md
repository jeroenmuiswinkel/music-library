# Music library API

This repo consists of a music library API made using FastAPI.

## How to run

### setting up the postgreSQL database

run the following command to create a postgreSQL docker container:

```sh
docker run --name=music-db-container -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=s3cret -e POSTGRES_DB=music-db -p 5432:5432 -d postgres
```

after the database container is running, we can add data to the container by running a python script that can be found in the music-library-data-ingestion repo.

Clone the code from that library, install the dependencies and run main.py:

```sh
pip install -r requirements.txt
```

```sh
python -m main
```

you should see the following messages in the terminal:

```
Connection established with PostgreSQL
Song table created successfully in PostgreSQL
Artist table created successfully in PostgreSQL
PostgreSQL connection is closed
```

the data is now loaded in the database and we can continue setting up redis.

### setting up Redis for caching

run the following command to create a redis docker container:

```sh
docker run --name=music-redis-container -d -p 6379:6379 redis
```

### Testing using Pytest

Now that both the database is running and filled with data, we can run our tests.

before we run our tests make sure that the TESTING variable in ./utils/const.py is set to True

Then run the following commands in the terminal:

```sh
pip install -r requirements.txt
```

```sh
python -m pytest tests
```

If everything went well then all tests pass.

### Running the application

Before running your API backend make sure the TESTING variable in ./utils/const.py is set to True.

The API application can now be run by using the following command:

```
python -m uvicorn app.main:app --reload
```

requests can be made by using the postman collection.

### Containerizing the API itself

If you want to containerize the API backend, that is also possible. Make sure the TESTING variable in ./utils/const.py is set to False.

The API backend can be containerized by running the following commands:

```sh
docker build -t music-library-api-image .
```

```sh
docker run -d --name music-library-api-container -p 8000:80 music-library-api-image
```

### Making requests

Requests can now be made using the postman collection. Besided that the openApi specifications can be seen at localhost:8000/docs

### Trouble shooting

If you are getting connection errors with the DB or with Redis after dockerizing the API this could be because the docker created IP addresses that are currently hardcoded in the ./utils/const.py file are wrong

for me the IP addresses are 172.17.0.2 and 172.17.0.3

You can check if they are different for you by running:

```
docker inspect <container id> | grep "IPAddress"
```
