"""
App initilizer.
"""

from fastapi import FastAPI

from users.routers import router as users_router
from authentication.routers import router as auth_router

app = FastAPI()

app.include_router(users_router)
app.include_router(auth_router)
