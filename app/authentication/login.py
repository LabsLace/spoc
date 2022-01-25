import hashlib

from fastapi import APIRouter, Depends
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.security import OAuth2PasswordRequestForm


from shared_functions.db_connection import execute_query
from shared_functions.spoc_logger import logger
from shared_functions.dependencies import manager


router = APIRouter()


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username, password = data.username, data.password
    salt = get_user_salt(username)

    if salt:
        password_hash = hash_password(salt, password)

        user_info = get_user_data(username, password_hash)
        if user_info:
            access_token = manager.create_access_token(data={"sub": user_info["email"]})

        else:
            raise InvalidCredentialsException

    else:
        raise InvalidCredentialsException

    return {"token": access_token, "user_info": user_info}


def get_user_salt(username):
    salt = None

    query = {
        "query": """
            SELECT
                salt
            FROM
                users.user_information
            WHERE
                username = %(username)s
        """,
        "params": {"username": username},
    }

    result = execute_query(query)

    if result["error"]:
        logger.warning("User salt not found in the DB.")

    else:
        if result["query_result"][0]:
            salt = result["query_result"][0][0]["salt"]

        else:
            salt = None

    return salt


def hash_password(salt, password):
    user_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 10000
    )
    return user_password.hex()


def get_user_data(username, password_hash):
    user_data = {}
    query = {
        "query": """
            SELECT
                username,
                first_name,
                email
            FROM
                users.user_information ui
            WHERE
                username = %(username)s
            AND
                password_hash = %(password_hash)s
        """,
        "params": {"username": username, "password_hash": password_hash},
    }

    result = execute_query(query)

    if result["error"]:
        logger.warning("Could not find user information to make login")

    else:
        query_result = result["query_result"][0]
        if query_result:
            user_data = query_result[0]

    return user_data
