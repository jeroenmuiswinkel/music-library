import json
from typing import List, Union

import caching.redis_object as re
from database.db_queries import (
    db_artist_id_exists,
    db_artist_name_exists,
    db_delete_artist,
    db_delete_song,
    db_get_artist_with_name,
    db_get_artists_of_genre,
    db_get_songs_of_genre,
    db_insert_artist,
    db_insert_song,
    db_patch_artist,
    db_patch_song,
    db_song_id_exists,
)
from fastapi import APIRouter, Body
from models.artist import Artist
from models.song import Song

app_v1 = APIRouter()


@app_v1.post("/song", tags=["song"])
async def post_song(song: Song):
    await db_insert_song(song)
    return {"result": "song is created"}


@app_v1.get("/song/genre", response_model=Union[List[Song], str], tags=["song"])
async def get_all_songs_of_genre(genre: str):
    # check if current request has already been cached in Redis
    redis_key = f"{genre}"
    redis_result = await re.redis.get(redis_key)

    if redis_result:
        return json.loads(redis_result.decode("utf-8"))

    # If not cached then a DB request will be made and the result will be cached
    # and then returned to the user.
    db_result = await db_get_songs_of_genre(genre)
    if db_result:
        await re.redis.set(redis_key, json.dumps(db_result).encode("utf-8"))
        return db_result
    else:
        return "no songs found for this genre"


@app_v1.patch("/song", tags=["song"])
async def patch_song(id: int, song: Song = Body(...)):
    if await db_song_id_exists(id):
        await db_patch_song(id, song)
        return {"result": "updated the song"}
    else:
        return {"result": "song id unknown"}


@app_v1.delete("/song", tags=["song"])
async def delete_song(id: int):
    if await db_song_id_exists(id):
        await db_delete_song(id)
        return {"result": "deleted the song"}
    else:
        return {"result": "song id unknown"}


@app_v1.post("/artist", tags=["artist"])
async def post_artist(name: str):
    if await db_artist_name_exists(name):
        return {"result": "artist name already exists"}
    else:
        await db_insert_artist(name)
        return {"result": "artist is created"}


@app_v1.get("/artist", response_model=Union[Artist, str], tags=["artist"])
async def get_artist(name: str):
    result = await db_get_artist_with_name(name)
    if result:
        return result
    else:
        return "No artist found"


@app_v1.get("/artist/genre", response_model=Union[str, List[str]], tags=["artist"])
async def get_all_artists_of_genre(genre: str):
    result = await db_get_artists_of_genre(genre)
    if result:
        return [song["artist"] for song in result]
    else:
        return "no artists found for this genre"


@app_v1.patch("/artist", tags=["artist"])
async def patch_artist(id: int, name: str):
    if await db_artist_id_exists(id):
        await db_patch_artist(id, name)
        return {"result": "updated the artist name"}
    else:
        return {"result": "artist id unknown"}


@app_v1.delete("/artist", tags=["artist"])
async def delete_artist(id: int):
    if await db_artist_id_exists(id):
        await db_delete_artist(id)
        return {"result": "deleted the artist"}
    else:
        return {"result": "artist id unknown"}
