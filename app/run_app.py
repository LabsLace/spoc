import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent.joinpath(".env"))

os.system("uvicorn --app-dir app main:app --reload")
