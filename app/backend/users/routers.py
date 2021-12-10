from fastapi import APIRouter
from pydantic import BaseModel, EmailStr

from users.create_users import create
from users.update_users import update


router = APIRouter()


class CreateUserInput(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str


@router.post("/users/", tags=["users"])
def create_users(user: CreateUserInput):
    create(user)


@router.get("/users/{user_uuid}", tags=["users"])
def update_users(user_uuid: str):
    update()
