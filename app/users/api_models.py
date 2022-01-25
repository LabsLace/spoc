from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class CreateUserInput(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: EmailStr


class UpdateUserInput(BaseModel):
    username: Optional[str] = ""
    password: Optional[str] = ""
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    email: Union[Optional[str], Optional[EmailStr]] = ""
