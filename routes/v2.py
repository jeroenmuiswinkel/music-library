from fastapi import APIRouter

app_v2 = APIRouter()


@app_v2.get("/", tags=["user"])
async def hello_world_v2():
    return {"request body: ": "this is version 2 of the API"}
