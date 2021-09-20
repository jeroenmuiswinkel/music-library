import asyncio

from app.main import app
from database.db_functions import execute, fetch
from database.db_object import db
from fastapi.testclient import TestClient

client = TestClient(app)
loop = asyncio.get_event_loop()

# before running all tests setup_module will connect to the DB
def setup_module():
    loop.run_until_complete(db.connect())


# after running all tests teardown_module will disconnect from the DB
def teardown_module():
    loop.run_until_complete(db.disconnect())


# check if artist name exists in DB
def check_get_artist(name):
    query = """select * from artist where name=:name"""
    values = {"name": name}

    result = loop.run_until_complete(fetch(query, True, values))
    return result is not None


# Test if Metallica exists in DB
def test_artist_exists():
    test_artist_name = "Metallica"
    assert check_get_artist(test_artist_name)


# Checks if a ArtistThatDoesNotExistsInDB does not exist in DB
def test_artist_does_not_exist():
    test_artist_name = "ArtistThatDoesNotExistsInDB"
    assert not check_get_artist(test_artist_name)
