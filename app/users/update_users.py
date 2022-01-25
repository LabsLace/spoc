import uuid
import hashlib

from fastapi.responses import JSONResponse

from shared_functions.db_connection import execute_query
from shared_functions.spoc_logger import logger


def update(user_uuid: str, user):
    """
    Idempotent function to update an user, the input is defined in the models
    and it will make the process to hash the password if needed and create
    the correct format of que query.
    """
    new_data_for_user = {key: value for key, value in user.dict().items() if value}

    if new_data_for_user:

        if new_data_for_user.get("password"):
            new_data_for_user = format_new_password(new_data_for_user)

        query = create_update_query(new_data_for_user, user_uuid)
        response = update_db(query)

    else:
        response = {
            "detail": [
                {"msg": "missing parameters to update user.", "status_code": 400}
            ]
        }

    return JSONResponse(response)


def format_new_password(user_data: dict):
    """
    If a new password is provided we need to do the same hash and salting as when we
    are creating a new user.
    """
    password = user_data.pop("password")
    user_data["salt"] = str(uuid.uuid4()).encode("utf-8")
    new_hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), user_data["salt"], 10000
    )
    user_data["password_hash"] = new_hashed_password

    return user_data


def create_update_query(query_params: dict, user_uuid: str):
    """
    Since we need to insert data depending on the parameters provided
    by the user in this function we create the query needed for that.
    """
    set_values = ""
    for key in query_params.keys():
        set_values += f"{key} = %({key})s, "
    set_values = set_values[:-2]

    query_params["user_uuid"] = user_uuid
    query = {
        "query": f"""
            UPDATE
                users.user_information
            SET
                {set_values}
            WHERE
                user_uuid = %(user_uuid)s
            RETURNING
                user_uuid,
                username,
                first_name,
                last_name,
                email
            """,
        "params": query_params,
    }

    return query


def update_db(query: dict):
    """
    Executes the correct query to update the user.
    """
    response = execute_query(query)

    if response["error"]:
        logger.error("Error while executing query: %s" % response)

    else:
        response = response["query_result"]

    return response
