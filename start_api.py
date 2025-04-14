from fastapi import FastAPI

from api import users

app = FastAPI()
app.include_router(users.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
