from fastapi import APIRouter

from shared_functions.spoc_logger import logger
from users.api_models import CreateUserInput, CreateUserOutput
from users.create_users import create
from users.update_users import update


router = APIRouter()


@router.post("/users/", response_model=CreateUserOutput, tags=["users"])
def create_users(user: CreateUserInput):
    logger.info("First event received to create user.")
    return create(user)


@router.get("/users/{user_uuid}", tags=["users"])
def update_users(user_uuid: str):
    update()
