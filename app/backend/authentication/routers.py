"""
Router to manage the authentication of the users to the app.
Some parts that we need to check are:
1. how are we goingo to keep trak of the sessions?
2. How is the frontend going to take care of the session?
3. how will each request will be checking that the session is valid?
4. How long will each session last?
"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from authentication.login import login
from shared_functions.dependencies import manager

router = APIRouter(tags=["authentication"])


@router.post("/login/")
def login_(data: OAuth2PasswordRequestForm = Depends()):
    """
    Handler to manage the login of the users.
    """
    return login(data)


@router.post("/logout/{user_uuid}", dependencies=[Depends(manager)])
def logout():
    """
    Handler to manage the logout of the users.
    """
    ...
