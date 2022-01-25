# pylint: disable-all
"""
General test for the function needed to connect to the DB.
"""
from unittest.mock import patch

import psycopg2.errorcodes
import psycopg2.errors

from app.shared_functions import execute_query


@patch("shared_functions.db_connection.psycopg2.connect")
def test_select_query(mock_connection):
    query = "SELECT * FROM users.user_information ui"
    mock_connection.return_value.cursor.return_value.fetchall.return_value = [
        {
            "id": 1,
            "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
            "email": "rod.mac.mad@gmail.com",
            "first_name": "Rodrigo",
            "last_name": "Macedo",
            "psw_hash": "123",
            "salt": "456",
            "created_tms": "2021-11-24 19:05:34.270177",
            "edited_tms": "2021-11-24 19:05:34.270177",
        },
        {
            "id": 2,
            "user_uuid": "9ae79854-9091-4109-ab8d-a89d1c812b04",
            "email": "test@yopmail.com",
            "first_name": "Test",
            "last_name": "Test",
            "psw_hash": "123",
            "salt": "4567",
            "created_tms": "2021-11-24 19:05:55.411820",
            "edited_tms": "2021-11-24 19:05:55.411820",
        },
    ]
    expected_result = {
        "error": False,
        "error_message": None,
        "query_result": [
            [
                {
                    "id": 1,
                    "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
                    "email": "rod.mac.mad@gmail.com",
                    "first_name": "Rodrigo",
                    "last_name": "Macedo",
                    "psw_hash": "123",
                    "salt": "456",
                    "created_tms": "2021-11-24 19:05:34.270177",
                    "edited_tms": "2021-11-24 19:05:34.270177",
                },
                {
                    "id": 2,
                    "user_uuid": "9ae79854-9091-4109-ab8d-a89d1c812b04",
                    "email": "test@yopmail.com",
                    "first_name": "Test",
                    "last_name": "Test",
                    "psw_hash": "123",
                    "salt": "4567",
                    "created_tms": "2021-11-24 19:05:55.411820",
                    "edited_tms": "2021-11-24 19:05:55.411820",
                },
            ]
        ],
    }
    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_select_with_params(mock_connection):
    query = {
        "query": """
            SELECT
                id,
                user_uuid,
                psw_hash
            FROM
                users.user_information
            WHERE
                id = %(id)s
            AND
                user_uuid = %(user_uuid)s
        """,
        "params": {"id": 1, "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29"},
    }
    mock_connection.return_value.cursor.return_value.fetchall.return_value = [
        {
            "id": 1,
            "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
            "psw_hash": "123",
        }
    ]
    expected_result = {
        "error": False,
        "error_message": None,
        "query_result": [
            [
                {
                    "id": 1,
                    "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
                    "psw_hash": "123",
                }
            ]
        ],
    }

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_select_with_identifiers(mock_connection):
    query = {
        "query": """
                SELECT
                    {id},
                    {user_uuid},
                    {psw_hash}
                FROM
                    {schema}.{table}
            """,
        "identifiers": {
            "id": "id",
            "user_uuid": "user_uuid",
            "psw_hash": "psw_hash",
            "schema": "users",
            "table": "user_information",
        },
    }
    mock_connection.return_value.cursor.return_value.fetchall.return_value = [
        {
            "id": 1,
            "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
            "psw_hash": "123",
        },
        {
            "id": 2,
            "user_uuid": "9ae79854-9091-4109-ab8d-a89d1c812b04",
            "psw_hash": "123",
        },
    ]
    expected_result = {
        "error": False,
        "error_message": None,
        "query_result": [
            [
                {
                    "id": 1,
                    "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
                    "psw_hash": "123",
                },
                {
                    "id": 2,
                    "user_uuid": "9ae79854-9091-4109-ab8d-a89d1c812b04",
                    "psw_hash": "123",
                },
            ]
        ],
    }

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_select_with_params_and_identifiers(mock_connection):
    query = {
        "query": """
            SELECT
                    {id},
                    {user_uuid},
                    {psw_hash}
                FROM
                    {schema}.{table}
            WHERE
                id = %(id)s
            AND
                user_uuid = %(user_uuid)s
        """,
        "params": {"id": 1, "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29"},
        "identifiers": {
            "id": "id",
            "user_uuid": "user_uuid",
            "psw_hash": "psw_hash",
            "schema": "users",
            "table": "user_information",
        },
    }
    mock_connection.return_value.cursor.return_value.fetchall.return_value = [
        {
            "id": 1,
            "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
            "psw_hash": "123",
        }
    ]
    expected_result = {
        "error": False,
        "error_message": None,
        "query_result": [
            [
                {
                    "id": 1,
                    "user_uuid": "9172edc5-bca7-4ed2-b714-3ffd40c1ba29",
                    "psw_hash": "123",
                }
            ]
        ],
    }

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_insert_query(mock_connection):
    query = {
        "query": """
            INSERT INTO users.user_information
            (
                email,
                first_name,
                last_name,
                psw_hash,
                salt
            )
            VALUES
            (
                %(email)s,
                %(first_name)s,
                %(last_name)s,
                %(psw_hash)s,
                %(salt)s
            )
        """,
        "params": {
            "email": "test@yopmail.com",
            "first_name": "Test",
            "last_name": "Test",
            "psw_hash": "123",
            "salt": "4567",
        },
    }
    mock_connection.return_value.cursor.return_value.description = None
    expected_result = {"error": False, "error_message": None, "query_result": []}

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_insert_with_identifiers(mock_connection):
    query = {
        "query": """
            INSERT INTO {schema}.{table}
            (
                email,
                first_name,
                last_name,
                psw_hash,
                salt
            )
            VALUES
            (
                %(email)s,
                %(first_name)s,
                %(last_name)s,
                %(psw_hash)s,
                %(salt)s
            )
        """,
        "params": {
            "email": "test@yopmail.com",
            "first_name": "Test",
            "last_name": "Test",
            "psw_hash": "123",
            "salt": "4567",
        },
        "identifiers": {"schema": "users", "table": "user_information"},
    }
    mock_connection.return_value.cursor.return_value.description = None
    expected_result = {"error": False, "error_message": None, "query_result": []}

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_insert_with_return(mock_connection):
    query = {
        "query": """
            INSERT INTO {schema}.{table}
            (
                email,
                first_name,
                last_name,
                psw_hash,
                salt
            )
            VALUES
            (
                %(email)s,
                %(first_name)s,
                %(last_name)s,
                %(psw_hash)s,
                %(salt)s
            )
            RETURNING id
        """,
        "params": {
            "email": "test@yopmail.com",
            "first_name": "Test",
            "last_name": "Test",
            "psw_hash": "123",
            "salt": "4567",
        },
        "identifiers": {"schema": "users", "table": "user_information"},
    }
    mock_connection.return_value.cursor.return_value.fetchall.return_value = [{"id": 9}]
    expected_result = {
        "error": False,
        "error_message": None,
        "query_result": [[{"id": 9}]],
    }

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_update_query(mock_connection):
    query = {
        "query": """
            UPDATE {schema}.{table}
            SET first_name = 'test_name'
            WHERE id = %(id)s
        """,
        "params": {"id": 9},
        "identifiers": {"schema": "users", "table": "user_information"},
    }
    mock_connection.return_value.cursor.return_value.description = None
    expected_result = {"error": False, "error_message": None, "query_result": []}

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_update_with_return(mock_connection):
    query = {
        "query": """
            UPDATE {schema}.{table}
            SET first_name = 'test_name'
            WHERE id = %(id)s
            RETURN id
        """,
        "params": {"id": 9},
        "identifiers": {"schema": "users", "table": "user_information"},
    }
    mock_connection.return_value.cursor.return_value.fetchall.return_value = [{"id": 9}]
    expected_result = {
        "error": False,
        "error_message": None,
        "query_result": [[{"id": 9}]],
    }

    result = execute_query(query)
    assert result == expected_result


@patch("shared_functions.db_connection.psycopg2.connect")
def test_non_existing_column(mock_connection):
    query = "SELECT i_don_exist FROM users.user_information"
    mock_connection.return_value.cursor.return_value.execute.side_effect = psycopg2.errors.UndefinedColumn(
        """column "i_don_exist" does not exist LINE 1: SELECT i_don_exist FROM users.user_information"""
    )
    expected_result = {
        "error": True,
        "error_message": """column "i_don_exist" does not exist LINE 1: SELECT i_don_exist FROM users.user_information""",
        "query_result": [],
    }

    result = execute_query(query)
    assert result == expected_result


def test_query_with_semicolon():
    query = "SELECT 'Hello World!';"
    expected_result = {
        "error": True,
        "error_message": "Something happened while trying to execute the queries",
        "query_result": [],
    }

    result = execute_query(query)
    assert result == expected_result
