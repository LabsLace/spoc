"""
NOTE: In the case of this module, the idea of the first log is to keep track of the flow of the api. We don't want to
log the incoming event because we can expose the password of the users.
"""

from fastapi import APIRouter

from shared_functions.spoc_logger import logger
from users.api_models import CreateUserInput, UpdateUserInput
from users.create_users import create
from users.update_users import update


router = APIRouter()


@router.post("/users/", tags=["users"])
def create_users(user: CreateUserInput):
    logger.info("First event received to create user.")
    return create(user)


@router.put("/users/{user_uuid}", tags=["users"])
def update_users(user_uuid: str, user: UpdateUserInput):
    logger.info("First event to update user received.")
    return update(user_uuid, user)
