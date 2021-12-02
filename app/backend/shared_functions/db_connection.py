"""
This functions should work for all the endpoints, the idea
is to have a unique place where we make connections to the DB.
"""


import os
import json
from typing import Union

import psycopg2
import psycopg2.extensions
import psycopg2.errorcodes
import psycopg2.errors
from cerberus import Validator
from psycopg2.extras import RealDictCursor
from psycopg2 import sql

from shared_functions.spoc_logger import logger

DB_NAME = os.environ["DB_NAME"]
HOST = os.environ["DB_HOST"]
PORT = os.environ["DB_PORT"]
USERNAME = os.environ["DB_USER"]
PASSWORD = os.environ["DB_PASSWORD"]


QUERY_SCHEMA = {
    "query": {"type": "string", "empty": False, "nullable": False, "required": True},
    "params": {"type": "dict", "empty": False, "nullable": True, "required": False},
    "identifiers": {
        "type": "dict",
        "empty": False,
        "nullable": True,
        "required": False,
    },
}


def execute_query(query: Union[str, list[dict], dict]) -> dict:
    """
    Main handler to execute queries, handles the logic and returns
    the correct response.
    """

    queries = prepare_queries_object(query)
    queries_results = {
        "error": True,
        "error_message": "Something happened while trying to execute the queries",
        "query_result": [],
    }

    if are_queries_valid(queries):
        executables = get_query_executables(queries)
        connection = get_connection()

        if connection:
            queries_results = execute(executables, connection)

        else:
            logger.error("Missing connection to execute queries.")

    return queries_results


def prepare_queries_object(query: Union[str, list[dict], dict]) -> list[dict]:
    """
    To work with one query or multiple queries this function generalize and
    creates a list of dictionaries.
    """
    queries = []

    if isinstance(query, str):
        queries = [{"query": query}]

    elif isinstance(query, dict):
        queries = [query]

    elif isinstance(query, list):
        queries = query

    else:
        raise TypeError

    return queries


def are_queries_valid(queries: list[dict]) -> bool:
    """
    We need to validate that the queries come in the correct format and also,
    be careful about the semicolons since they can lead to SQL injection
    problems
    """
    is_valid = True
    query_validator = Validator(QUERY_SCHEMA)

    for query in queries:
        if not query_validator.validate(query) or ";" in query["query"]:
            is_valid = False

    return is_valid


def get_query_executables(queries: list[dict]) -> list[dict]:
    """
    Formats the queries, adds identifiers and create the tuples of the complete
    data that will be executed.
    """
    executables = []

    for query in queries:
        identifiers = query.get("identifiers")
        sql_query_obj = sql.SQL(query["query"])

        if identifiers:
            identifiers = {
                key: sql.Identifier(value) for key, value in identifiers.items()
            }
            sql_query_obj = sql_query_obj.format(**identifiers)

        params = query.get("params", {})

        executables.append((sql_query_obj, params))

    return executables


def get_connection() -> psycopg2.extensions.connection:
    """
    If we have valid queries we can create the connection to the DB.
    Returning a real dict cursor since it will return the rows as
    dictionaries.
    """

    connection = None

    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            host=HOST,
            port=PORT,
            user=USERNAME,
            password=PASSWORD,
            cursor_factory=RealDictCursor,
        )

    except psycopg2.OperationalError:
        logger.error("Couldn't connect to the DB.")

    return connection


def execute(
    queries_executables: list[tuple], connection: psycopg2.extensions.connection
) -> list[dict]:
    """
    Make the call to the DB and returns the last response with the
    result.
    """
    # TODO:  We are missing a lot of exceptions but let's add them as we need.
    error, error_message, queries_result = False, None, []
    cursor = connection.cursor()

    for executable_data in queries_executables:
        try:
            cursor.execute(executable_data[0], executable_data[1])

        except psycopg2.errors.lookup(psycopg2.errorcodes.UNDEFINED_TABLE) as exception:
            error, error_message = True, str(exception)
            connection.rollback()

        except psycopg2.errors.lookup(
            psycopg2.errorcodes.UNDEFINED_COLUMN
        ) as exception:
            error, error_message = True, str(exception)
            connection.rollback()

        else:
            if cursor.description is not None:
                result = json.loads(json.dumps(cursor.fetchall(), default=str))
                queries_result.append(result)

    if connection:
        connection.commit()
        connection.close()

    return {
        "error": error,
        "error_message": error_message,
        "query_result": queries_result,
    }
