from pydantic import BaseModel, EmailStr


class CreateUserInput(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr


class CreateUserOutput(BaseModel):
    username: str
    first_name: str
    email: EmailStr
