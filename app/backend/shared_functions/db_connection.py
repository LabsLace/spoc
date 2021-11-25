"""
Get env variables to make the correcto connection to the DB.
Get query or queries from the client
Check if the query is a string or the queries is a list of dictionaries
    or if the query is a dictionary:
    E.g: query = "Select..."
    query = [
        {
            "query": "Select..."  # Not optional
            "identifiers: {"column_name": "name", " # Optional
            "parameters": {"}
        }
    ]

    query = {
        "query": "Select..."  # Not optional
        "identifiers: {"column_name": "name", " # Optional
        "parameters": {"}
    }

If the query is not a valid type:
    raise or return and error

if the query is a valid type:

    if the query is a str it can be executes (means it does not have parameters or identifiers)

    if the query is a list of dicts of a dictionary:
        convert dict to list of dictionaries:

        for each dict in the list of dicts:
            if it has identifirs:
                format query

            if it has parameters
                format query

        return formatted queries

after format queries
    get connection or raise

    if connection:
        for query in queries:
            # Needs to return a dictionary and append to a list,
            # it does not matter if it is just one query
            # Handle status codes and errors
            # If one query fails it should return an error and prevent any commit to the DB.
            result = execute_query(query)

    return result [
        "status_code": 200,
        "error": True/False,
        "error_message": None/"message",
        "query_result": [{}, {}, {}, {}, {}, {}]
    ]

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


# Remove for after and testing debugging
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv(
#     dotenv_path="/Users/rodrigomacedo/Documents/LACE/code_projects/spoc/app/backend/.env"
# )


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

FORBIDDEN_COMMANDS = ["DELETE", "DROP"]


def execute_query(query: Union[str, list[dict], dict]) -> dict:
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
            ...

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
    is_valid = True
    query_validator = Validator(QUERY_SCHEMA)

    for query in queries:
        if not query_validator.validate(query) or ";" in query["query"]:
            is_valid = False

    return is_valid


def get_query_executables(queries: list[dict]) -> list[dict]:
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
        ...

    return connection


def execute(
    queries_executables: list[tuple], connection: psycopg2.extensions.connection
) -> list[dict]:
    error, error_message, queries_result = False, None, []
    cursor = connection.cursor()

    for executable_data in queries_executables:
        try:
            cursor.execute(executable_data[0], executable_data[1])

        except psycopg2.errors.lookup(psycopg2.errorcodes.UNDEFINED_TABLE) as exception:
            error, error_message = True, exception

        else:
            result = json.loads(json.dumps(cursor.fetchall()))
            queries_result.append(result)

    return {
        "error": error,
        "error_message": error_message,
        "query_result": queries_result,
    }
