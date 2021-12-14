import uuid
import hashlib

from shared_functions.db_connection import execute_query
from shared_functions.spoc_logger import logger


def create(user):
    """
    Entry point of the code after receiving the event from the the client.
    """
    user_body = user.dict()
    user_body = format_user_password(user_body)
    user_body = format_parameters_for_db(user_body)
    create_user_in_db(user_body)
    return user


def format_user_password(body):
    """
    Creates salt for the password of the user and encrypts the password
    that will be stored in the DB.
    """
    body["salt"] = str(uuid.uuid4()).encode("utf-8")
    user_password = hashlib.pbkdf2_hmac(
        "sha256", body["password"].encode("utf-8"), body["salt"], 10000
    )
    body["password_hash"] = user_password
    return body


def format_parameters_for_db(body):
    """
    Remove and add the data needed to execute the query to insert into the DB.
    """
    body.pop("password")
    body["user_uuid"] = str(uuid.uuid4())
    return body


def create_user_in_db(body):
    """
    Execute query to insert the values in the DB.
    """
    query = {
        "query": """
            INSERT INTO users.user_information (
                user_uuid,
                username,
                first_name,
                last_name,
                email,
                salt,
                password_hash
            )
            VALUES(
                %(user_uuid)s,
                %(username)s,
                %(first_name)s,
                %(last_name)s,
                %(email)s,
                %(salt)s,
                %(password_hash)s
            )
        """,
        "params": body,
    }

    response = execute_query(query)
    if response["error"]:
        logger.error("Error while executing query: %s" % response)
