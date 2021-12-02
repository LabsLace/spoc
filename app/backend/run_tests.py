"""
File to run all the tests in the backend directory.
"""

import os

import pathlib
from dotenv import load_dotenv

load_dotenv(dotenv_path=pathlib.Path(__file__).parent.joinpath(".env"))

os.system("python -m pytest app/backend -vvv")
