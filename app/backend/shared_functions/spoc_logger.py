"""
Main logger for the app.
"""
import logging
import re


def get_logger():
    """
    Creates a logger with a handler that formats the messages,
    with this we are able to handle the logs as JSON trying to make easier the debugging.
    """
    flask_logger = logging.getLogger("uvicorn.error")
    flask_logger.setLevel(logging.ERROR)
    logger_ = logging.getLogger()
    logger_.setLevel(logging.INFO)
    logger_.handlers = []
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    format_ = """{"time":"%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s",
    file_name": "%(filename)s", "lineno": "%(lineno)s"} """.replace(
        "\n", ""
    )
    format_ = re.sub(" +", " ", format_)
    formatter = logging.Formatter(format_)
    stream_handler.setFormatter(formatter)

    logger_.addHandler(stream_handler)

    return logger_


logger = get_logger()
