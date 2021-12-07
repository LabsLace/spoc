"""
App initilizer.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from shared_functions.spoc_logger import logger

load_dotenv(dotenv_path=Path(__file__).parent.joinpath(".env"))

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
