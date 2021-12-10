"""
App initilizer.
"""
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from users.routers import router as users_router

load_dotenv(dotenv_path=Path(__file__).parent.joinpath(".env"))

app = FastAPI()

app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
