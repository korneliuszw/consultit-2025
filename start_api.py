from fastapi import FastAPI

from api import users, downtimes, infrastructure, invoices, customers, subscription

app = FastAPI()
app.include_router(users.router)
app.include_router(downtimes.router)
app.include_router(infrastructure.router)
app.include_router(invoices.router)
app.include_router(customers.router)
app.include_router(subscription.router)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
