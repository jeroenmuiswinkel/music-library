import aioredis
import caching.redis_object as re
from database.db_object import db
from fastapi import FastAPI
from routes.v1 import app_v1
from routes.v2 import app_v2
from utils.const import REDIS_URL

app = FastAPI(
    title="Music API Documentation",
    description="This API can be used to get information on songs and artists",
    version="1.0.0",
)

# API Version 1
app.include_router(app_v1, prefix="/v1")

# API Version 2
app.include_router(app_v2, prefix="/v2")


# on startup, connect to DB and redis
@app.on_event("startup")
async def connect_db():
    await db.connect()
    re.redis = await aioredis.from_url(REDIS_URL, encoding="utf-8")


# on shutdown, disconnect from DB and redis
@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()

    re.redis.close()
    await re.redis.wait_closed()
