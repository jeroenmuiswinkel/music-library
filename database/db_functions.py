from database.db_object import db


async def execute(query, values=None):
    await db.execute(query=query, values=values)


async def fetch(query, is_one, values=None):
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        out = None if result is None else dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        out = None if result is None else [dict(row) for row in result]

    return out
