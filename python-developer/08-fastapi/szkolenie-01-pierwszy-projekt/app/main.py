from fastapi import FastAPI
from app.routers import users

app = FastAPI(title="Moje API", version="1.0.0")

app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Witaj w API!"}
