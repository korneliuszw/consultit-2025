from fastapi import FastAPI

from api import users, downtimes, infrastructure

app = FastAPI()
app.include_router(users.router)
app.include_router(downtimes.router)
app.include_router(infrastructure.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
