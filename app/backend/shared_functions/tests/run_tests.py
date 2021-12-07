"""
File to run all the tests in the backend directory.
"""

import os

import pathlib
from dotenv import load_dotenv

load_dotenv(dotenv_path=pathlib.Path(__file__).parent.parent.parent.joinpath(".env"))

os.system("pytest --pyargs app/backend/shared_functions -vvv")
