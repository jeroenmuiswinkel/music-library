from database.db_functions import execute, fetch


# Song queries
async def db_insert_song(song):
    query = """
    insert into song(name, year, artist, shortname, bpm, duration, genre, spotifyid, album)
    values(:name, :year, :artist, :shortname, :bpm, :duration, :genre, :spotifyid, :album )
    """
    values = dict(song)

    await execute(query, values)


async def db_get_songs_of_genre(genre):
    query = """
    select * from song where genre=:genre
    """
    values = {"genre": genre}

    return await fetch(query, False, values)


async def db_song_id_exists(id):
    query = """
    select * from song where id=:id
    """
    values = {"id": id}
    result = await fetch(query, True, values)
    return result is not None


async def db_patch_song(id, song):
    query = """
    update song set name=:name, year=:year,artist=:artist, shortname=:shortname, bpm=:bpm, duration=:duration, genre=:genre, spotifyid=:spotifyid, album=:album
    where id=:id
    """
    values = dict(song)
    values.update({"id": id})
    await execute(query, values)


async def db_delete_song(id):
    query = """
    delete from song 
    where id=:id
    """
    values = {"id": id}
    await execute(query, values)


# Artist queries
async def db_insert_artist(name):
    query = """
    insert into artist(name)
    values(:name)
    """
    values = {"name": name}

    await execute(query, values)


async def db_artist_name_exists(name):
    query = """
    select * from artist where name = :name
    """
    values = {"name": name}
    result = await fetch(query, True, values)
    return result is not None


async def db_get_artist_with_name(name):
    query = """
    select * from artist where name=:name
    """
    values = {"name": name}

    return await fetch(query, True, values)


async def db_get_artists_of_genre(genre):
    query = """
    select distinct artist from song where genre=:genre
    """
    values = {"genre": genre}
    return await fetch(query, False, values)


async def db_artist_id_exists(id):
    query = """
    select * from artist where id = :id
    """
    values = {"id": id}
    result = await fetch(query, True, values)
    return result is not None


async def db_patch_artist(id, name):
    query = """
    update artist set name=:name 
    where id=:id
    """
    values = {"id": id, "name": name}
    await execute(query, values)


async def db_delete_artist(id):
    query = """
    delete from artist 
    where id=:id
    """
    values = {"id": id}
    await execute(query, values)
