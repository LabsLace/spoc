"""
App initilizer.
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask
from shared_functions.spoc_logger import logger

load_dotenv(dotenv_path=Path(__file__).parent.joinpath(".env"))

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

if __name__ == "__main__":
    logger.info("Running app.")
    app.run()
