import os

from fastapi_login import LoginManager

SECRET_KEY = os.environ["SECRET_KEY"]

manager = LoginManager(SECRET_KEY, "/login")
